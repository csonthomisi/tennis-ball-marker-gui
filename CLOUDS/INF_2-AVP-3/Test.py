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
cloud=cloud[(cloud[:,0]<20)&(cloud[:,1]<20)&(cloud[:,2]<10)&(cloud[:,0]>-10)&(cloud[:,1]>-10)&(cloud[:,2]>-10)]

x = cloud[:,0]
y = cloud[:,1]
z = cloud[:,2]
fig = mlab.figure(figure='Pointcloud', bgcolor=(1, 1, 1), fgcolor=None, engine=None, size=(1000, 500))
mlab.points3d(x, y, z, color=(0, 0, 0), mode="point", colormap="afmhot", figure=fig)
mlab.points3d(0.0, 0.0, 0.0, mode="sphere", scale_factor=0.3)
mlab.points3d(9.37671304, 16.4997886,  -2.17378488, color=(1,0,0),mode="cube", scale_factor=0.2) # Ball 0 position

mlab.show()


""" Test inverting transformation"""

original_point=np.array([0,0,0])
R=np.array([[ 0.49258322, -0.87021818,  0.00906036],
            [-0.02185534, -0.00196203,  0.99975922],
            [-0.86999087, -0.49266264, -0.01998538]])
T=np.array([[-5.34338244], [ 1.95500662], [18.10892334]])
R_T=np.vstack((np.hstack((R, T)),[0,0,0,1]))
print(R_T)

fig = mlab.figure(figure='Pointcloud', bgcolor=(1, 1, 1), fgcolor=None, engine=None, size=(1000, 500))
mlab.points3d(original_point[0], original_point[1], original_point[2], color=(0, 0, 0), mode="sphere", colormap="afmhot", figure=fig)



def transform(rotation, translation, point):
    P=np.array(point)
    P=P[0:3]
    points=np.reshape(P,(3,1))
    rot=np.array(rotation).reshape(3,3)
    tr=np.array(translation).reshape(3,1)
    transformed_points=rot.dot(points)+tr
    return transformed_points

transformed_point=transform(R, T, original_point)
print(transformed_point)
mlab.points3d(transformed_point[0], transformed_point[1], transformed_point[2], color=(1, 0, 0), mode="sphere", colormap="afmhot", figure=fig)


inverse_R=R.T
inverse_T=np.matmul(-R.T,T)
print(inverse_T)

back_transformed_point=transform(inverse_R, inverse_T, transformed_point)
print(back_transformed_point)
mlab.points3d(back_transformed_point[0], back_transformed_point[1], back_transformed_point[2], color=(0,1, 0), mode="sphere", colormap="afmhot", figure=fig)


mlab.show()
print(R, T)
print(inverse_R, inverse_T)