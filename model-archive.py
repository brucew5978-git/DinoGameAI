import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
from collections import OrderedDict
from torch.nn import init


def conv3x3(inChannels, outChannels, stride=1, padding=1, bias=True, groups=1):
    return nn.Conv2d(
        inChannels,
        outChannels,
        kernel_size=3,
        stride=stride,
        padding=padding,
        bias=bias,
        groups=groups
    ) 

def conv1x1(inChannels, outChannels, groups=1):
        return nn.Conv2d(
        inChannels,
        outChannels,
        kernel_size=1,
        stride=1,
        groups=groups
    ) 

def channelShuffle(x, groups):
    batchsize, numChannels, height, width = x.data.size()

    channelsPerGroup = numChannels // groups

    #Reshape
    x = x.view(batchsize, groups, channelsPerGroup, height, width)

    x = torch.transpose(x, 1, 2).contiguous()

    #flatten tensor
    x = x.view(batchsize, -1, height, width)

    return x


class ShuffleUnit(nn.Module):
    def __init__(self, inChannels, outChannels, groups=3, groupedConv=True, combine='add'): 
        super().__init__()

        self.inChannels = inChannels
        self.outChannels = outChannels
        self.groupedConv = groupedConv
        self.combine = combine
        self.groups = groups
        self.bottleneckChannels = self.outChannels//4

        #Define type of ShuffleUnit used
        if self.combine == 'add':
            self.depthwiseStride = 1
            self.combineFunc = self._add