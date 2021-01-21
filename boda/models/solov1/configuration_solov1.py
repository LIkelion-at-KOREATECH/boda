import os
from typing import Sequence, Union, Any
from ...base_configuration import BaseConfig


solov1_pretrained_models = {
    'solov1-base': '',
    'solov1': ''
}


class Solov1Config(BaseConfig):
    """Configuration for SOLOv1

    Arguments:
        max_size ():
        padding ():
        proto_net_structure (List):
    """
    config_name = 'solov1'

    def __init__(
        self,
        num_classes: int = 80,
        max_size=550,
        selected_layers: Sequence[int] = [1, 2, 3],
        fpn_channels: int = 256,
        num_extra_fpn_layers: int = 1,
        scales=[[8, 32], [16, 64], [32, 128], [64, 256], [128, 512]],
        grids=[40, 36, 24, 16, 12],
        strides: Sequence[int] = [4, 8, 16, 32, 64],
        base_edges=[16, 32, 64, 128, 256],
        **kwargs
    ) -> None:
        super().__init__(max_size=max_size, **kwargs)
        self.num_classes = num_classes + 1
        self.selected_layers = selected_layers
        self.fpn_channels = fpn_channels
        self.num_extra_fpn_layers = num_extra_fpn_layers
        self.scales = scales
        self.grids = grids
        self.strides = strides
        self.base_edges = base_edges

        self.cate_down_pos = 0

