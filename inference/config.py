import os
import json
import warnings

    
class Config:
    
    _PARAMS = {}
    
    def __init__(self, config=None, **kwargs):
        
        if isinstance(config, Config):
            return config
        
        self._set_default_params()
        
        if isinstance(config, dict):
            self._update(**config)
        self._update(**kwargs)
        
    def __str__(self):
        config = self.to_dict()
        return json.dumps(config, indent=2)
    
    def __repr__(self):
        config = self.to_dict()
        return str(config)

    def _set_default_params(self):
        self._update(**self._PARAMS)
        
    def _update(self, **kwargs):
        for param, value in kwargs.items():
            if param.upper() in self._PARAMS:
                setattr(self, param.upper(), value)
            else:
                raise ValueError('Not supported parameter: "{}". Supported parameters: {}'.format(
                                        param, ', '.join(self._PARAMS)))
                
    def to_dict(self):
        config = {}
        for param in self._PARAMS:
            config[param] = getattr(self, param)
        return config
    
    def save(self, path, overwrite=False, indent=None):
        if os.path.isdir(path):
            path = os.path.join(path, 'config.json')
            
        if os.path.exists(path) and not overwrite:
            warnings.warn('File have NOT been saved because it is already exists, set overwtire=True!')
        else:
            config = self.to_dict()
            with open(path, 'w') as f:
                json.dump(config, f, indent=indent)
    
    @classmethod
    def load_config(cls, path):
        if os.path.isdir(path):
            path = os.path.join(path, 'config.json')
        with open(path, 'r') as f:
            json_config = json.load(f)
            config = dict(json_config)
        return cls(config)
    
class OrthoSegmModelConfig(Config):
    
    # should be uppercase!
    _PARAMS = {
        'CHANNELS': [],                   # list of channels e.g. ["RED", "BLU"]
        'CLASSES': [],                    # list of classes e.g. ["0100", "0200"]
        'GSD': [1, 1],                    # list [gsd_x, gsd_y]
        'INPUT_SHAPE': None,              # list [H, W], specify only if your model needs exact inpus size
        'TRAIN_INPUT_SHAPE': [],          # list [H, W] used during training
        'STANDARDISING_FUNCTIONS': [],    # list of function names for input standartisation
        'STANDARDISING_PARAMS': {},       # dict of parameters for input standartisation
    }


class DatasetElementConfig(Config):
    # should be uppercase!
    _PARAMS = {
        'CHANNELS': [],  # list of channels e.g. ["RED", "BLU"]
        'CLASSES': [],  # list of classes e.g. ["0100", "0200"]
        'GSD': [1., 1.],  # list [gsd_x, gsd_y]
        'INPUT_SHAPE': None,  # list [H, W], specify only if your model needs exact inpus size
        'TRAIN_INPUT_SHAPE': [],  # list [H, W] used during training
        'STANDARDISING_FUNCTIONS': [],  # list of function names for input standartisation
        'STANDARDISING_PARAMS': {},  # dict of parameters for input standartisation
    }