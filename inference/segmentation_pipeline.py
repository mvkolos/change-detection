from backend.constants import SEGMENTATION_MODEL_PATH
from .model import load_model
import os
import matplotlib.pyplot as plt

class SegmentationPipeline:
    model = None
    data = None
    def __init__(self):
        if self.model is None:
            self._load_model()
    def _load_model(self):
        self.model = load_model(SEGMENTATION_MODEL_PATH)

    def predict(self, opm):
        if self.model is None:
            self._load_model()
        mask, transform_matrix = self.model.predict_orthophoto(opm)

        plt.imsave(os.path.join(opm,'mask.png'), mask)
        return 'ok'
