from threading import Thread
import numpy as np
import base64
import flask
# import redis
import uuid
import time
import json
import sys
import io
import os
from flask_cors import CORS
from inference.segmentation_pipeline import SegmentationPipeline
from backend.constants import APP_STATIC, OPM_VOLUME
from backend.geoserver_manager import post_geotiff
# from flask_uploads import UploadSet, configure_uploads, IMAGES
from PIL import Image

# UploadSet
# #from flask.ext.uploads import UploadSet, configure_uploads, IMAGES
#
# photos = UploadSet('photos', IMAGES)

# initialize constants used for server queuing
IMAGE_QUEUE = "image_queue"
BATCH_SIZE = 2
SERVER_SLEEP = 0.25
CLIENT_SLEEP = 0.25

APP_ROOT = os.path.dirname(os.path.abspath(__file__))  # refers to application_top

app = flask.Flask(__name__, static_folder=APP_STATIC)
CORS(app)
# db = redis.StrictRedis(host="localhost", port=6379, db=0)
RESOURCES = 'backend\\resources'


@app.route('/')
def hb():
    return 'alive'


# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')
# def catch_all(path):
#    if app.debug:
#        return requests.get('http://localhost:8080/{}'.format(path)).text
#    return render_template("index.html")


# if this is the main thread of execution first load the model and
# then start the server
def inference_():
    print("* Loading model...")
    # model load
    print("* Model loaded")

    # continually pool for new images to classify
    while True:
        # attempt to grab a batch of images from the database, then
        # initialize the image IDs and batch of images themselves
        # queue = db.lrange(IMAGE_QUEUE, 0, BATCH_SIZE - 1)
        # imageIDs = []
        # batch = None
        #
        # # loop over the queue
        # for q in queue:
        #     # deserialize the object and obtain the input image
        #     q = json.loads(q.decode("utf-8"))
        #     #PREPROCESS
        #     # image = base64_decode_image(q["image"], IMAGE_DTYPE,
        #     #                             (1, IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_CHANS))
        #     #rasterio processing
        #     # check to see if the batch list is None
        #     # if batch is None:
        #     #     batch = image
        #
        #     # otherwise, stack the data
        #     # else:
        #     #     batch = np.vstack([batch, image])
        #
        #     # update the list of image IDs
        #     imageIDs.append(q["id"])
        #
        # # check to see if we need to process the batch
        # if len(imageIDs) > 0:
        #     # classify the batch
        #     #PREDICT
        #     print("* Batch size: {}".format(batch.shape))
        #     #preds = model.predict(batch)
        #
        #     # loop over the image IDs and their corresponding set of
        #     # results from our model
        #     #FORMAT OUTPUT
        #     # for (imageID, resultSet) in zip(imageIDs, results):
        #     #     # initialize the list of output predictions
        #     #     output = []
        #     #
        #     #     # loop over the results and add them to the list of
        #     #     # output predictions
        #     #     for (imagenetID, label, prob) in resultSet:
        #     #         r = {"label": label, "probability": float(prob)}
        #     #         output.append(r)
        #     #
        #     #     # store the output predictions in the database, using
        #     #     # the image ID as the key so we can fetch the results
        #     #     db.set(imageID, json.dumps(output))
        #
        #     # remove the set of images from our queue
        #     db.ltrim(IMAGE_QUEUE, len(imageIDs), -1)

        # sleep for a small amount
        time.sleep(SERVER_SLEEP)


@app.route('/file')
def get_file():
    path = flask.request.args.get('path')
    filename = flask.request.args.get('filename')
    base_url = os.path.join(APP_STATIC, path)
    return flask.send_from_directory(base_url, filename)


@app.route('/datasets', methods=['POST'])
def post_dataset():
    dataset_name = flask.request.args.get('datasetName')

    if dataset_name is None:
        dataset_name = 'ds'
    dataset_base_dir = os.path.join(OPM_VOLUME
                                    , dataset_name)
    if not os.path.exists(dataset_base_dir):
        os.makedirs(dataset_base_dir)
    if 'filePre' in flask.request.files and 'filePost' in flask.request.files:
        image_pre = Image.open(flask.request.files['filePre'])
        image_post = Image.open(flask.request.files['filePost'])
        file_pre = os.path.join(dataset_base_dir, '{}_0_pre.tif'.format(dataset_name))
        file_post = os.path.join(dataset_base_dir,'{}_0_post.tif'.format(dataset_name))
        image_pre.save(file_pre)
        image_post.save(file_post)
        post_geotiff(file_pre, '{}_0_pre'.format(dataset_name))
        post_geotiff(file_post, '{}_0_post'.format(dataset_name))
    else:
        raise Exception()
    if 'fileMarkup' in flask.request.files:
        image_markup = Image.open(flask.request.files['fileMarkup'])
        file_markup = os.path.join(dataset_base_dir, '{}_0_gt.tif'.format(dataset_name))
        image_markup.save(file_markup)
        post_geotiff(file_markup, '{}_0_gt'.format(dataset_name))
    return dataset_name


@app.route('/datasets', methods=['GET'])
def fetch_datasets():
    datasets_dir = os.path.join(APP_STATIC, 'datasets')
    datasets = os.listdir(datasets_dir)
    print(datasets)
    configs = []
    for dataset in datasets:
        config_path = os.path.join(datasets_dir, dataset, 'config.json')
        with open(config_path, 'r') as config:
            js = json.loads(config.read())
            js['coverUrl'] = 'http://localhost:5000/file?path=datasets/{}&filename=background.png'.format(dataset)
            print(js)
            configs.append(js)
    response = {
        'datasets': configs
    }
    return flask.jsonify(response)


@app.route('/datasets/<dataset_id>/series', methods=['GET'])
def fetch_series(dataset_id):
    print(dataset_id)
    datasets_dir = os.path.join(APP_STATIC, 'datasets', dataset_id)
    series_ids = [file for file in os.listdir(datasets_dir) if os.path.isdir(os.path.join(datasets_dir, file))]
    print(series_ids)
    series = [{'seriesId': seriesId,
               'layerPre': get_layer(dataset_id, seriesId, 0),
               'layerPost': get_layer(dataset_id, seriesId, 1)} for seriesId in series_ids]
    response = {
        'series': series
    }
    return flask.jsonify(response)


def get_layer(dataset_id, series_id, postfix):
    return 'opm-host:{dataset_id}_{series_id}_{postfix}'.format(dataset_id, series_id, postfix)


@app.route('/test_model', methods=['POST'])
def test():
    pipeline = SegmentationPipeline()
    return pipeline.predict(os.path.join(APP_STATIC, 'datasets', 'ventura_000000'))


if __name__ == "__main__":
    # load the function used to classify input images in a *separate*
    # thread than the one used for main classification
    # print("* Starting model service...")
    # t = Thread(target=inference, args=())
    # t.daemon = True
    # t.start()

    # start the web server
    print("* Starting web service...")
    app.run(host='0.0.0.0', debug=True)
    d = {'g': 'hh'}
    # db.rpush(IMAGE_QUEUE, json.dumps(d))
