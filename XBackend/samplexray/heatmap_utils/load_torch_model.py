import re
import os

import torch

from .torch_densenet import DenseNet121

nnClassCount =14
pathModel = os.path.join(os.getcwd() + "/samplexray/heatmap_utils/torchmodel/densenet.pth.tar")

def build_model():
    #Initialize the network
    model = DenseNet121(nnClassCount, True).cuda()
    print(pathModel)
        
    model = torch.nn.DataParallel(model).cuda()

    modelCheckpoint = torch.load(pathModel)
    state_dict =modelCheckpoint['state_dict']
    
    #modify:
    # '.'s are no longer allowed in module names, but pervious _DenseLayer
    # has keys 'norm.1', 'relu.1', 'conv.1', 'norm.2', 'relu.2', 'conv.2'.

    #So, let's write some Regex code to fix this issue

    pattern = re.compile(
        r'^(.*denselayer\d+\.(?:norm|relu|conv))\.((?:[12])\.(?:weight|bias|running_mean|running_var))$')
    
    for key in list(state_dict.keys()):
        res = pattern.match(key)
        if res:
            new_key = res.group(1) + res.group(2)
            state_dict[new_key] = state_dict[key]
            del state_dict[key]
    model.load_state_dict(state_dict)

    #For visualising the final convolutional layer we will define the 
    # model to be the convolutional base(densenet121)

    model = model.module.densenet121.features
    model.eval()

    return model