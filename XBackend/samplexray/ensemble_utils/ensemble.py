import os
import cv2
import pickle
import numpy as np
from matplotlib import pyplot as plt
from keras.models import model_from_json
from keras.applications.xception import preprocess_input as pi_xception
from keras.applications.inception_resnet_v2 import preprocess_input as pi_irnv2
import keras.backend.tensorflow_backend as tb

class Ensemble():

    CURRENT_DIR = os.getcwd()

    PATH_W = os.path.join(CURRENT_DIR + '/ensemble-content/ensemble_normalized_weights.pkl')
    PATH_THRESH = os.path.join(CURRENT_DIR + '/ensemble-content/thresholds.npy')

    with open(PATH_W, 'rb') as fp:
        NORM_WEIGHTS = pickle.load(fp)
    THRESHOLDS = np.load(PATH_THRESH)

    MODEL_NAMES = ['xception', 'irnv2', 'dn121', 'dn169', 'dn201']

    PATHS_ARCH = {
        'xception' : '/model-architectures/architecture_xception.json',
        'irnv2'    : '/model-architectures/architecture_irnv2.json',
        'dn121'    : '/model-architectures/architecture_dn121.json',
        'dn169'    : '/model-architectures/architecture_dn169.json',
        'dn201'    : '/model-architectures/architecture_dn201.json'
    }

    PATHS_WEIGHTS = {
        'xception' : '/model-weights/xception.h5',
        'irnv2'    : '/model-weights/irnv2.h5',
        'dn121'    : '/model-weights/dn121.h5',
        'dn169'    : '/model-weights/dn169.h5',
        'dn201'    : '/model-weights/dn201.h5'
    }

    PREPROCESS_INPUTS = {
        'xception' : pi_xception,
        'irnv2'    : pi_irnv2,
        'dn121'    : None,
        'dn169'    : None,
        'dn201'    : None
    }

    MODELS = {
        'xception' : None,
        'irnv2'    : None,
        'dn121'    : None,
        'dn169'    : None,
        'dn201'    : None
    }

    def build_models(self):
        tb._SYMBOLIC_SCOPE.value = True
        for model_name in self.MODEL_NAMES: 
            json_file = open(os.path.join(self.CURRENT_DIR + self.PATHS_ARCH[model_name]), 'r')
            model_architecture = json_file.read()
            json_file.close()
            model = model_from_json(model_architecture)
            model.load_weights(os.path.join(self.CURRENT_DIR + self.PATHS_WEIGHTS[model_name]))
            self.MODELS[model_name] = model
            print(model_name + "BUILT AND LOADED")

    def preprocess(self, raw_img, preproc_func = None):
        img = cv2.resize(raw_img, (224, 224))
        if preproc_func != None:
            img = preproc_func(img)
        else: 
            img = img/255.
        img = img.reshape(1, 224, 224, 3)
        return img

    def get_probabilities(self, raw_img):
        predictions = {
            'xception' : None,
            'irnv2'    : None,
            'dn121'    : None,
            'dn169'    : None,
            'dn201'    : None
        }
        for model_name in self.MODEL_NAMES: 
            img = self.preprocess(raw_img, preproc_func = self.PREPROCESS_INPUTS[model_name])
            model = self.MODELS[model_name]
            predictions[model_name] = model.predict(img)[0]

        return predictions

    def get_predictions(self, IMG_PATH):
        tb._SYMBOLIC_SCOPE.value = True
        raw_img = cv2.imread(IMG_PATH)
        probabilities = self.get_probabilities(raw_img)

        for model_name in ['dn169', 'dn201']:
            temp = np.empty(probabilities[model_name].shape)
            temp[0] = probabilities[model_name][0]
            temp[1] = probabilities[model_name][2]
            temp[2] = probabilities[model_name][3]
            temp[3] = probabilities[model_name][1]
            temp[4] = probabilities[model_name][4]
            probabilities[model_name] = temp

        sum = 0
        for model_name in self.MODEL_NAMES:
            sum += probabilities[model_name] * self.NORM_WEIGHTS[model_name]

        ensembled_predictions = sum/len(self.MODEL_NAMES)
        y_hat = ensembled_predictions > self.THRESHOLDS
        
        return np.array(list(y_hat)).astype(int)
