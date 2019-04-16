from DiagramlayerTopLevel import Diagramlayer as levelsetdgm

import torch
import torch.nn as nn
import numpy as np
from scipy.spatial import Delaunay

class LevelSetLayer(nn.Module):
    """
    Level set persistence layer
    Parameters:
        size : (width, height) - tuple for image input dimensions
        maxdim : haximum homology dimension (default 1)
    """
    def __init__(self, size, maxdim=1):
        super(LevelSetLayer, self).__init__()
        self.size = size
        self.maxdim = maxdim
        self.fnobj = levelsetdgm()

        # extract width and height
        width, height = size
        # initialize complex to use for persistence calculations
        axis_x = np.arange(0, width)
        axis_y = np.arange(0, height)
        grid_axes = np.array(np.meshgrid(axis_x, axis_y))
        grid_axes = np.transpose(grid_axes, (1, 2, 0))

        # creation of a complex for calculations
        tri = Delaunay(grid_axes.reshape([-1, 2]))
        faces = tri.simplices.copy()
        self.complex = self.fnobj.init_filtration(faces)

    def forward(self, img):
        dgm = self.fnobj.apply(img, self.complex)
        dgm = dgm[0:(self.maxdim+1),:,:]
        return dgm
