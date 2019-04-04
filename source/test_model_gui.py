import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential, Model
from keras.layers import Conv2D, MaxPooling2D, BatchNormalization
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.preprocessing import image
from keras.utils import to_categorical
from keras import backend as K
from keras.models import load_model
import cv2
import scipy as sp

class TestDemo:
    def __init__(self):
        self.img_height = 180
        self.img_width = 150
        self.Categories = ['Normal', 'Pneumonia']

    def model_load(self):
        print("Please insert the filepath of the model")
        self.model_filepath = "Pneumonia_Project_180x150_Data_model_for_CAM.h5"
        self.model = load_model(self.model_filepath)
        return self.model

    def plot_cam(self, W, pred, fmaps, img_resized):
        self.w = W[:, pred]

        self.cam = fmaps.dot(self.w)
        self.cam = sp.ndimage.zoom(self.cam, (21.4, 36), order=1) #21.4, 36

        plt.subplot(1,1,1)
        plt.imshow(img_resized, alpha = 0.8)
        plt.imshow(self.cam, cmap='jet', alpha=0.5)
        plt.show()

    def create_cam_model_plt(self, filepath, model):
        self.activation_layer = model.get_layer('activation_132')
        self.cam_model = Model(inputs = model.input, outputs = self.activation_layer.output)
        self.final_dense = model.get_layer('dense_1')
        self.W = self.final_dense.get_weights()[0]

        self.img = cv2.imread(filepath)
        self.img_resized = cv2.resize(self.img, (180, 150))
        self.img_dims_right = np.array(self.img_resized).reshape(-1, 180, 150, 3)

        self.fmaps = self.cam_model.predict(self.img_dims_right)[0]
        self.probs = self.model.predict(self.img_dims_right)
        self.pred = np.argmax(self.probs[0])

        if self.probs == [[1]]:
            self.plot_cam = TestDemo().plot_cam(self.W, self.pred, self.fmaps, self.img_resized)

        

    def test_img(self, filepath):

        print("Please insert the filepath of the image")
        self.img = cv2.imread(filepath)
        self.img_resized = cv2.resize(self.img, (self.img_height, self.img_width))
        self.img_dims_right = np.array(self.img_resized).reshape(-1, self.img_height, self.img_width, 3)
        self.predict = self.model.predict(self.img_dims_right)
        self.result = str(self.Categories[int(self.predict[0][0])])  + " " + str(int(self.predict[0][0]))
        return  self.result 

if __name__ == '__main__':
    pass