#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 17:05:09 2020

@author: mcsontho
"""

import numpy as np
import mayavi.mlab as mlab


cloud = np.loadtxt("50th_frame_points.txt").reshape((-1,3))
print(cloud)

x = cloud[:,0]
y = cloud[:,1]
z = cloud[:,2]
fig = mlab.figure(figure='Pointcloud', bgcolor=(1, 1, 1), fgcolor=None, engine=None, size=(1000, 500))
mlab.points3d(x, y, z, color=(0, 0, 0), mode="point", colormap="afmhot", figure=fig)
#mlab.points3d(0.0, 0.0, 0.0, mode="sphere", scale_factor=0.3)
#mlab.points3d(-1.07, 0.015, -1.35, mode="cube", scale_factor=0.2) # IMU position
mlab.show()