import os
import numpy as np
from PIL import Image
import cv2

import torch
import torch.nn as nn
import torch.backends.cudnn as cudnn
import torchvision
import torchvision.transforms as transforms


# Class Activation Map code for plotting activation Heatmaps of different 
# anomaly regions in the supplied X-Ray

class HeatmapGenerator ():
    
    def __init__ (self, model):

        self.model = model

        self.imageSize =224       
        
        #Initialize the weights
        self.weights = list(self.model.parameters())[-2]

        #Initialize the image transform - resize and normalize
        normalize = transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        transformList = []
        transformList.append(transforms.Resize(self.imageSize))
        transformList.append(transforms.ToTensor())
        transformList.append(normalize)      
        
        self.transformSequence = transforms.Compose(transformList)
   

    def generate (self, pathImageFile, pathOutputFile):
        
        #Load image, transform, convert 
        imageData = Image.open(pathImageFile).convert('RGB')
        imageData = self.transformSequence(imageData)
        imageData = imageData.unsqueeze_(0)
        input = torch.autograd.Variable(imageData)
        
        self.model.cuda()
        output = self.model(input.cuda())
        
        #Generate heatmap, on class based Activation
        heatmap = None
        for i in range (0, len(self.weights)):
          map = output[0,i,:,:]
          if i == 0: heatmap = self.weights[i] * map
          else: heatmap += self.weights[i] * map
        
        #Blend the images
        npHeatmap = heatmap.cpu().data.numpy()

        imgOriginal = cv2.imread(pathImageFile, 1)
        imgOriginal = cv2.resize(imgOriginal, (self.imageSize, self.imageSize))
        
        cam = npHeatmap / np.max(npHeatmap)
        cam = cv2.resize(cam, (self.imageSize, self.imageSize))
        heatmap = cv2.applyColorMap(np.uint8(255*cam), cv2.COLORMAP_TURBO)
              
        img = heatmap * 0.5 + imgOriginal
            
        cv2.imwrite(pathOutputFile, img)