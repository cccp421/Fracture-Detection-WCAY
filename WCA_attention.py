import torch
from torch import nn


class WCA(nn.Module):
    # Weight Coordinate Attention
    def __init__(self, channels) -> None:
        super().__init__()

        self.gap = nn.Sequential(
            nn.AdaptiveAvgPool2d((1, 1)),
            Conv(channels, channels)
        )
        self.pool_h = nn.AdaptiveAvgPool2d((None, 1))
        self.pool_w = nn.AdaptiveAvgPool2d((1, None))
        self.conv_hw = Conv(channels, channels, (3, 1))
        self.conv_pool_hw = Conv(channels, channels, 1)

    def forward(self, x):
        _, _, h, w = x.size()
        x_pool_h, x_pool_w = self.pool_h(x), self.pool_w(x).permute(0, 1, 3, 2)
        x_pool_hw = torch.cat([x_pool_h, x_pool_w], dim=2)
        x_pool_hw = self.conv_hw(x_pool_hw)
        x_pool_h, x_pool_w = torch.split(x_pool_hw, [h, w], dim=2)
        x_pool_hw_weight = self.conv_pool_hw(x_pool_hw).sigmoid()
        x_weight, y_weight = torch.split(x_pool_hw_weight, [h, w], dim=2)
        x_pool_h, x_pool_w = x_pool_h * x_weight, x_pool_w * y_weight
        a_h = x_pool_h.sigmoid()
        a_w = x_pool_w.permute(0, 1, 3, 2).sigmoid()
        out = x * a_h * a_w
        return out