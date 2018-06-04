"""

Model is a wrapper over a set of KERAS models!
implements interface for learning over a generator + dataset or statically generated data
and for prediction (for all classes)

"""

import os
import cv2
import json
import keras
import rasterio
import numpy as np
from keras.utils import generic_utils
from keras.models import Model
from functools import wraps
import geojson

from .utils import get_shape
from .utils import pad_shape, unpad
from .utils import overlap_split
from .utils import overlap_concatenate

from .config import OrthoSegmModelConfig
from .standardizer import Standardizer


def _create_dir(*args):
    path = os.path.join(*args)
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def _find_weights(weights_dir, mode='last'):
    """Find weights path if not provided manually during model initialization"""

    if mode == 'last':
        file_name = sorted(os.listdir(weights_dir))[-1]
        weights_path = os.path.join(weights_dir, file_name)

    elif mode == 'best':
        raise NotImplementedError
    else:
        raise NotImplementedError

    return weights_path


def _find_model(model_chkp_dir, mode='last'):
    """Find weights path if not provided manually during model initialization"""

    if mode == 'last':
        file_name = sorted(os.listdir(model_chkp_dir))[-1]
        model_path = os.path.join(model_chkp_dir, file_name)

    elif mode == 'best':
        raise NotImplementedError

    return model_path


def load_model(model_dir, mode='inference', config_path='auto', graph_path='auto',
               weights_path='auto', model_path='auto', custom_objects=None):
    if config_path == 'auto':
        config_path = os.path.join(model_dir, 'config.json')

    if graph_path == 'auto':
        graph_path = os.path.join(model_dir, 'graph.json')

    if weights_path == 'auto':
        weights_dir = os.path.join(model_dir, 'weights')
        weights_path = _find_weights(weights_dir)

    if model_path == 'auto':
        model_chkp_dir = os.path.join(model_dir, 'models')
        model_path = _find_model(model_chkp_dir)

    # load configuration file
    config = OrthoSegmModelConfig.load_config(config_path)

    # load model graph file
    with open(graph_path, 'r') as f:
        graph = json.load(f)

    if mode == 'train':
        model = keras.models.load_model(model_path, custom_objects=custom_objects, compile=True)
    if mode == 'inference':
        try:
            model = keras.models.load_model(model_path, custom_objects=custom_objects, compile=False)
        except:
            model = keras.models.model_from_json(json.dumps(graph))
            model.load_weights(weights_path)

    segmentation_model = SegmentationModel(model_dir)
    segmentation_model.build(model, config)

    return segmentation_model


class SegmentationModel(Model):
    """


    """

    def __init__(self, model_dir):

        self.config = None
        self.model = None
        self._built = False

        self.model_dir = _create_dir(model_dir)
        self.log_dir = _create_dir(model_dir, 'log')
        self.weights_dir = _create_dir(model_dir, 'weights')
        self.models_dir = _create_dir(model_dir, 'models')  # be careful with model and models! dirs

        # input standardization pipeline function
        self._input_standart = None

    def __getattr__(self, attr):
        return getattr(self.model, attr)

    def build(self, model, config):
        self.model = model
        self.config = config

        # save configurations of model
        config_path = os.path.join(self.model_dir, 'config.json')
        if not os.path.exists(config_path):
            self.config.save(config_path, indent=2)

        # save graph of model
        graph_path = os.path.join(self.model_dir, 'graph.json')
        model_graph = json.loads(model.to_json())
        with open(graph_path, 'w') as f:
            json.dump(model_graph, f, indent=2)

        st = Standardizer(**self.config.STANDARDISING_PARAMS)
        self._input_standart = st.build_pipline(self.config.STANDARDISING_FUNCTIONS)

        self._built = True

    def built(func):
        @wraps(func)
        def wrapped(self, *args, **kwargs):
            if self._built:
                return func(self, *args, **kwargs)
            else:
                raise RuntimeError('Your model is not built! Please provide keras model and config.')

        return wrapped

    @built
    def _get_gsd(self):
        gsd = self.config.GSD
        if np.isscalar(gsd):
            gsd = (gsd, gsd)

        gsd_x = gsd[0]
        gsd_y = gsd[1]
        return gsd_x, gsd_y

    @built
    def _load_image(self, path, target_size=None, return_transform=False, return_crs=True):
        dataset_element_name = os.path.basename(path)
        path = os.path.normpath(path)
        channels = self.config.CHANNELS
        target_gsd_x, target_gsd_y = self._get_gsd()

        # defining local variables for memorizing best of them during iterations
        transform = None
        crs = None
        min_gsd_x = 10e5
        min_gsd_y = 10e5
        gsd_x = min_gsd_x
        gsd_y = min_gsd_y
        max_h = 0
        max_w = 0

        image_ids = ['20170304', '20170404']
        channels_list = []

        for image_id in image_ids:
            channels_ = [os.path.join(path, image_id, '{}_channel_{}.tif'.format(dataset_element_name, ch)) for ch in
                         channels]
            for channel_name in channels_:
                try:
                    # open image(channel) file
                    # use 'r+' mode to support on windows >__<
                    # (otherwise, in 'r' mode, cv2.resize fails with python int to C int conversion overflow)
                    with rasterio.open(channel_name, 'r+') as img_obj:

                        # read metadata from image(channel) file
                        tm = list(img_obj.transform)
                        gsd_x = np.sqrt(tm[0] ** 2 + tm[3] ** 2)
                        gsd_y = np.sqrt(tm[1] ** 2 + tm[4] ** 2)

                        crs = img_obj.crs

                        # remember best gsd and h and w for future resizing
                        if gsd_x * gsd_y < min_gsd_x * min_gsd_y:
                            transform = tm
                            min_gsd_x = gsd_x
                            min_gsd_y = gsd_y
                            max_h = img_obj.height
                            max_w = img_obj.width

                        # read channels
                        img = img_obj.read()
                        img = np.squeeze(img)
                        channels_list.append(img)

                except FileNotFoundError:
                    print('No such image {}'.format(os.path.basename(channel_name)))
                    raise Exception('No channels!')

            # define width and heights of our images for our model gsd
            w = int(max_w * gsd_x / target_gsd_x)
            h = int(max_h * gsd_y / target_gsd_y)

            if target_size:
                w = target_size[1]
                h = target_size[0]
        channels_list = [cv2.resize(ch, (w, h), cv2.INTER_LINEAR) for ch in channels_list]

        image = np.array(channels_list)
        image = np.rollaxis(image, 0, 3)
        if return_transform:
            if return_crs:
                return image, transform, crs
            else:
                return image, transform

        return image

    @built
    def _load_masks(self, path):

        path = os.path.normpath(path)
        classes = self.config.CLASSES

        mask_id = os.path.basename(path)
        masks = [os.path.join(path, '{}_class_{}.tif'.format(mask_id, cls)) for cls in classes]

        masks_list = []
        for m, cls in zip(masks, classes):
            try:
                with rasterio.open(m, 'r') as mask_obj:
                    mask = mask_obj.read()
                    mask = np.squeeze(mask)
                    masks_list.append(mask)
            except FileNotFoundError:
                print('No such image {}'.format(os.path.basename(m)))
                raise Exception('No mask for class {}!'.format(cls))

        masks = np.array(masks_list)
        masks = np.rollaxis(masks, 0, 3)
        #         if target_size:
        #             cv2.resize(masks, target_size, cv2.INTER_NEAREST)

        return masks

    def _to_binary_masks(self, image, tm):
        gsd_x, gsd_y = self._get_gsd()

        target_gsd_x = np.sqrt(tm[0] ** 2 + tm[3] ** 2)
        target_gsd_y = np.sqrt(tm[1] ** 2 + tm[4] ** 2)

        # define width and heights of our masks for our model gsd
        w = int(image.shape[1] * gsd_x / target_gsd_x)
        h = int(image.shape[0] * gsd_y / target_gsd_y)
        image = cv2.resize(image, (w, h), cv2.INTER_LINEAR)

        if image.ndim == 2:
            image = np.expand_dims(image, axis=-1)

        return np.rollaxis(image, 2, 0), (w, h)

    @built
    def _save_raster_masks(self, image, path, save_postfix='pred', transform_matrix=None,
                           crs=None):
        image, shape = self._to_binary_masks(image, transform_matrix)

        path = os.path.normpath(path)  # delete '\' or '//' in the end of filepath
        if not os.path.exists(path):
            os.makedirs(path)
        w, h = shape

        image_basename = os.path.basename(path)

        saved_images_names = []

        for i, cls in enumerate(self.config.CLASSES):
            # save each mask to separate file
            image_name = image_basename + '_class_{}_{}.tif'.format(cls, save_postfix)
            saved_images_names.append(image_name)
            image_path = os.path.join(path, image_name)
            with rasterio.open(image_path, 'w', width=w, height=h, driver='GTiff', count=1,
                               dtype='uint8', NBITS=1, transform=transform_matrix[:6], crs=crs) as dst:
                dst.write(image[i].astype(rasterio.uint8), 1)

        return saved_images_names

    def get_vector_markup(self, mask, geotransform, trg_crs='epsg:3857'):
        """
        Saves vector mask from raw model output as .geojson
        :param raw_mask_path:
        :param transform: geotransform of initial dataset
        :param filename: output location absolute path
        :param trg_crs: target coordinate reference system
        :param threshold: a threshold for raw mask low-pass filtering
        :return:
        """

        # plt.imsave(os.path.join(time_series_path, time_frame, '_'.join([dataset_element_name, mask_name, time_frame, self.get_timestamp()])+'.png'), raw)
        shapes = rasterio.features.shapes(mask, transform=geotransform)
        # the last shape contains all geometry
        shapes = list(shapes)[:-1]
        polygons = [geojson.Feature(geometry=geojson.Polygon(shape[0]['coordinates'])) for shape in shapes]
        crs = {
            "type": "name",
            "properties": {
                "name": trg_crs}}
        gs = geojson.FeatureCollection(polygons, crs=crs)
        return geojson.dumps(gs)

    @built
    def _save_vector_masks(self, image, path, save_postfix='pred', geotransform=None, trg_crs='epsg:3857',
                           threshold=170):
        image, shape = self._to_binary_masks(image, geotransform)
        path = os.path.normpath(path)  # delete '\' or '//' in the end of filepath
        if not os.path.exists(path):
            os.makedirs(path)

        image_basename = os.path.basename(path)

        saved_geojson_names = []

        for i, cls in enumerate(self.config.CLASSES):
            # save each mask to separate file
            image_name = image_basename + '_class_{}_{}.geojson'.format(cls, save_postfix)
            saved_geojson_names.append(image_name)
            image_path = os.path.join(path, image_name)
            image_mask = np.array(image[i] > threshold, np.uint8)
            gs = self.get_vector_markup(image_mask, geotransform, trg_crs)
            with open(image_path, 'w') as file:
                file.write(gs)

        return saved_geojson_names

    @built
    def _standardize(self, image):
        return self._input_standart(image)

    @built
    def predict_orthophoto(self, path_to_object, split_size=1024,
                           overlap=64, save=False, save_dir='same', verbose=0):

        image, transform_matrix, crs = self._load_image(path_to_object, return_transform=True,
                                                        return_crs=True)
        h, w = image.shape[:2]

        h = get_shape(h, split_size, overlap)
        w = get_shape(w, split_size, overlap)

        image, paddings = pad_shape(image, (h, w))
        images, n_rows, n_cols = overlap_split(image, split_size, overlap)

        predictions = []
        progbar = generic_utils.Progbar(len(images), verbose=verbose)
        if verbose:
            print('Predicting image pieces...')

        for image in images:
            image = self._standardize(image)
            image = np.expand_dims(image, axis=0)  # input image have to be 4d tensor
            pred = self.model.predict(image)
            pred = np.squeeze(pred)  # delete useless 0 axis
            predictions.append(pred)
            progbar.add(1)

        if len(predictions) > 1:
            prediction = overlap_concatenate(predictions, n_rows, n_cols, overlap)
        else:
            prediction = np.squeeze(predictions)

        prediction = unpad(prediction, paddings)

        if save:
            if save_dir == 'same':
                save_dir = path_to_object
            round_prediction = np.round(prediction)
            self._save_masks(round_prediction, save_dir, transform_matrix=transform_matrix, crs=crs)

        return prediction, transform_matrix
