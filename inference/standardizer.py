import numpy as np

class Standardizer(object):

    epsilon = np.array(0.00001)
    
    def __init__(self, mean=0, std=1, scale=255):
        self.mean = np.array(mean)
        self.std = np.array(std)
        self.scale = np.array(scale)
        
    def _pipline(self, functions, x):
        for func in functions:
            if not callable(func):
                func = getattr(self, func)
            x = func(x)
        return x
    
    def build_pipline(self, functions):
        def pipline(x):
            return self._pipline(functions, x)
        return pipline
    
    def rescale(self, x):
        return x / self.scale
        
    def featurewise_center(self, x):
        return x - self.mean

    def featurewise_std_normalization(self, x):
        return x / (self.std + self.epsilon)

    def samplewise_center(self, x):
        axes = tuple(range(x.ndim))[:-1]
        return x - np.mean(x, axis=axes)
        
    def samplewise_std_normalisation(self, x):
        axes = tuple(range(x.ndim))[:-1]
        return x / (np.std(x, axis=axes) + self.epsilon)