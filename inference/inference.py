from .model import load_model
from .dataset_element_vrt import DatasetElementVRT

class Inference:
    pipeline = None
    dataset_element = None
    def __init__(self, sources, config):
        self.dataset_element = DatasetElementVRT(sources, config)

    def _load_model(self, model_path):
        self.model = load_model(model_path)

