
import sys
from typing import Tuple, List, Dict, Any
import numpy as np
from torch import nn, Tensor

from .architecture_base import PreTrainedModel


class Yolov1PredictNeck(nn.Module):
    """Prediction Neck for Yolov4
    Arguments:
        selected_layers (List[float]):
        scales (List[float]):
    Returns:
        List[Tensor]
    """
    def __init__(self, config, **kwargs) -> None:
        self.selected_layers = kwargs.get('selected_layers')
        self.scales = kwargs.get('scales')
        raise NotImplementedError
    
    def forward(self, inputs) -> List[Tensor]:
        outputs = inputs
        return outputs


class Yolov1PredictHead(nn.Module):
    def __init__(self, config, **kwargs) -> None:
        self.config = config
        self.out_channles = 5 * config.num_boxes + config.num_classes
        
        self.fc = nn.Sequential(
            nn.Conv2d(2048, 1024, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(1024, 1024, kernel_size=3, stride=2, padding=1),
            nn.ReLU(),

            nn.Conv2d(1024, 1024, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(1024, 1024, kernel_size=3, padding=1),
            nn.ReLU())

        self.classifier = nn.Sequential(
            nn.Linear(self.grid_size * self.grid_size * 1024, 4096),
            nn.ReLU(),
            nn.Linear(4096, self.grid_size * self.grid_size * self.out_channels),
            nn.Sigmoid())
        )
        self._initialize_weights()

    def forward(self, inputs: List[Tensor]) -> List[Tensor]:
        
        outputs = inputs
        return outputs


class Yolov1PreTrainedModel(PreTrainedModel):
    def _init_weights(self, module):
        """ Initialize the weights """
        if isinstance(module, (nn.Linear, nn.Embedding)):
            # Slightly different from the TF version which uses truncated_normal for initialization
            # cf https://github.com/pytorch/pytorch/pull/5617
            module.weight.data.normal_(mean=0.0, std=self.config.initializer_range)
        elif isinstance(module, nn.LayerNorm):
            module.bias.data.zero_()
            module.weight.data.fill_(1.0)
        if isinstance(module, nn.Linear) and module.bias is not None:
            module.bias.data.zero_()


class Yolov1Model(Yolov1PreTrainedModel):
    """
    ██╗   ██╗ ██████╗ ██╗      ██████╗ 
    ╚██╗ ██╔╝██╔═══██╗██║     ██╔═══██╗
     ╚████╔╝ ██║   ██║██║     ██║   ██║██╗   ██╗
      ╚██╔╝  ██║   ██║██║     ██║   ██║╚██╗ ██╔╝ 
       ██║   ╚██████╔╝███████╗╚██████╔╝ ╚████╔╝    
       ╚═╝    ╚═════╝ ╚══════╝ ╚═════╝   ╚═══╝

    The only specificity that we require is that the dataset 
    __getitem__ should return:

    Arguments:
        image: a PIL Image of size (H, W)
        target: a dict containing the following fields
            boxes (FloatTensor[N, 4]): the coordinates of the N bounding boxes 
                in [x0, y0, x1, y1] format, ranging from 0 to W and 0 to H
            labels (Int64Tensor[N]): the label for each bounding box. 0 represents 
                always the background class.
            image_id (Int64Tensor[1]): an image identifier. It should be unique 
                between all the images in the dataset, and is used during evaluation
            area (Tensor[N]): The area of the bounding box. This is used during 
                evaluation with the COCO metric, to separate the metric scores between small, medium and large boxes.
            iscrowd (UInt8Tensor[N]): instances with iscrowd=True will be ignored 
                during evaluation.
    """
    def __init__(self, config, backbone=None) -> None:
        self.config = config
        if isinstance(config.max_size, tuple):
            self.max_size = config.max_size
        else:
            self.max_size = (config.max_size, config.max_size)
        if backbone is None:
            self.backbone = DarkNetBackbone(config)
        self.head = Yolov1PredictHead(config)

        self._init_weights()

        raise NotImplementedError

    def forward(self, inputs: List[Tensor]) -> List[Tensor]:
        if self.head.training:
            inputs = self.check_inputs(inputs)
            return inputs
        
        

        outputs = inputs
        return outputs

    def initialize_weights(self, path):
        raise NotImplementedError

    


    