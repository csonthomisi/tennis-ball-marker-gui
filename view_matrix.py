#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 11 11:42:43 2020

@author: mcsontho
"""
import numpy as np
import mayavi.mlab as mlab
import transforms3d
def transform(rotation, translation, point):
    P=np.array(point)
    P=P[0:3]
    points=np.reshape(P,(3,1))
    rot=np.array(rotation).reshape(3,3)
    tr=np.array(translation).reshape(3,1)
    transformed_points=rot.dot(points)+tr
    return transformed_points


def view(balls, B2L, case_avp1):
    if case_avp1:
        cloud = np.loadtxt("CLOUDS/INF_1-AVP-1/50th_frame_points.txt").reshape((-1,3))
    else:
        cloud = np.loadtxt("CLOUDS/INF_2-AVP-3/50th_frame_points.txt").reshape((-1,3))
#    print(cloud)
    cloud=cloud[(cloud[:,0]<20)&(cloud[:,1]<20)&(cloud[:,2]<10)&(cloud[:,0]>-10)&(cloud[:,1]>-10)&(cloud[:,2]>-10)]
    
    x = cloud[:,0]
    y = cloud[:,1]
    z = cloud[:,2]
    fig = mlab.figure(figure='Pointcloud', bgcolor=(1, 1, 1), fgcolor=None, engine=None, size=(1000, 500))
    mlab.points3d(x, y, z, color=(0, 0, 0), mode="point", colormap="afmhot", figure=fig)
    mlab.points3d(0.0, 0.0, 0.0, mode="sphere", scale_factor=0.3)
    # Calculate balls_new
    
    
    from itertools import repeat
    
    balls_new=np.array(list(map(transform, repeat(B2L[:3,:3]), repeat(B2L[:3,3]), balls)))
#    print("Ballse_new_2", balls_new_2)
#    print("New points", balls_new)
    balls_x=balls_new[:,0]
    balls_y=balls_new[:,1]
    balls_z=balls_new[:,2]
    mlab.points3d(balls_x, balls_y, balls_z, color=(1,0,0),mode="sphere", scale_factor=0.2) # Ball 0 position
    print("[0,0,0] ball in Lidar system\n",transform(B2L[:3,:3], B2L[:3,3], [0,0,0]))
    mlab.show()
    return balls_new
    