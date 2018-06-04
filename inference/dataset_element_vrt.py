import rasterio
from rasterio.vrt import WarpedVRT
import rasterio.features
import geojson
import numpy as np
import cv2
import os

def v_print(verbose):
    def f(*args, **kwargs):
        if verbose:
            print (*args, **kwargs)
    return f

class DatasetElementVRT:

    def __init__(self, sources = [], config = None):
        '''
        :param sources: a list of binary images
        :param config: dictionary with gsd, number of classes
        '''
        self.sources = sources
        self.config = config
        self.image = self.get_image()

    def get_gsd(self):
        if self.config is None:
            raise Exception('No config found')
        gsd = self.config.GSD
        if np.isscalar(gsd):
            gsd = (gsd, gsd)

        gsd_x = gsd[0]
        gsd_y = gsd[1]
        return gsd_x, gsd_y
    def reshape_to_target_gsd(self, img, tm):

        gsd_x, gsd_y = abs(tm[0]), abs(tm[4])
        target_gsd_x, target_gsd_y = self.get_gsd()

        if abs(gsd_x - target_gsd_x) / target_gsd_x > 0.1 or \
                                abs(gsd_y - target_gsd_y) / target_gsd_y > 0.1:
            h, w = img.shape[:2]
            w = int(w * gsd_x / target_gsd_x)
            h = int(h * gsd_y / target_gsd_y)
            print(w, h, gsd_x, gsd_y)
            img = cv2.resize(img, (w, h), cv2.INTER_NEAREST)
            tm = [target_gsd_x, tm[1], tm[2], tm[3], -target_gsd_y, tm[5]]

        return img, tm
    def get_image(self):
        if len(self.sources)==0:
            return None
        #reading all images and their transforms
        images = [self.imread(img) for img in self.sources]
        #
        m_image, m_crs, m_tm = max(images, key = lambda image: image[0].shape[-1]*image[0].shape[-2])
        channels = []
        for image in images:
            image_channels = image[0]
            num_channels = image_channels.shape[0]
            channels += list(np.squeeze(np.split(image_channels, num_channels, axis = 0)))
        channels, tm = self.upsample_channels(channels, m_image.shape[1:], m_tm)
        self.tm = tm
        self.crs = m_crs
        return channels

    def imread(self, image):
        '''
        Reads an image from stream
        :param image:
        :return:
        '''
        source = self.reproject(image)
        crs = source.crs
        print(crs)
        transform = list(source.transform)[:6]
        img = source.read().squeeze()
        return img, crs, transform

    def upsample_channels(self, channels, shape, tm):
        '''
        Upsamples all channels to the maximum resolution
        :param channels:
        :return:
        '''
        #print(shape)
        h, w = shape
        # resize all images to max resolution
        print ('Resizing to max resolution {}px x {}px ... '.format(h,w), end='')
        upsampled_channels = [cv2.resize(channel, (w, h), cv2.INTER_NEAREST) for channel in channels]
        print('done!')

        image = np.stack(upsampled_channels, axis=-1)
        #print(tm)
        print('Resizing to target resolution gsd_x={:.5}, gsd_y={:.5} ... '.format(*self.get_gsd()), end='')
        print()
        image, tm = self.reshape_to_target_gsd(image, tm)
        print('done!')

        return image, tm
    def reproject(self, source, dst_crs = 'epsg:3857'):
        with rasterio.open(source) as src:
            reprojected = WarpedVRT(src, dst_crs = dst_crs)
        return reprojected
    def to_binary_masks(self,image, tm):
        gsd_x, gsd_y = self._get_gsd()

        target_gsd_x = np.sqrt(tm[0] ** 2 + tm[3] ** 2)
        target_gsd_y = np.sqrt(tm[1] ** 2 + tm[4] ** 2)

        # define width and heights of our masks for our model gsd
        w = int(image.shape[1] * gsd_x / target_gsd_x)
        h = int(image.shape[0] * gsd_y / target_gsd_y)
        image = cv2.resize(image, (w, h), cv2.INTER_LINEAR)

        if image.ndim == 2:
            image = np.expand_dims(image, axis=-1)

        return np.rollaxis(image, 2, 0), (w,h)

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
    def get_vector_markup(self,mask, geotransform, trg_crs = 'epsg:3857'):
        """
        Saves vector mask from raw model output as .geojson
        :param raw_mask_path:
        :param transform: geotransform of initial dataset
        :param filename: output location absolute path
        :param trg_crs: target coordinate reference system
        :param threshold: a threshold for raw mask low-pass filtering
        :return:
        """

        #plt.imsave(os.path.join(time_series_path, time_frame, '_'.join([dataset_element_name, mask_name, time_frame, self.get_timestamp()])+'.png'), raw)
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

    def _save_vector_masks(self, image, path, save_postfix='pred', geotransform=None, trg_crs = 'epsg:3857', threshold = 170):
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
            image_mask = np.array(image[i]>threshold, np.uint8)
            gs = self.get_vector_markup(image_mask, geotransform, trg_crs)
            with open(image_path, 'w') as file:
                file.write(gs)

        return saved_geojson_names
