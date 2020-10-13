#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 14:26:28 2020

@author: mcsontho
"""
import numpy as np

def project_to_image(points, proj_mat):
    proj_mat=np.real(proj_mat)
    num_pts = points.shape[1]
    points = np.vstack((points, np.ones((1, num_pts))))
    points = proj_mat @ points
    points[:2, :] /= points[2, :]
    return points[:2, :]


im_size=[720,1280]
def project_2_image(pts, calib):
    # Pixels from 3D points
    pts_2d = project_to_image(pts[:,0:3].T, calib)
    global im_size
    img_width=im_size[1]
    img_height=im_size[0]
    # Filter lidar points to be within image FOV
    infov = np.where((pts_2d[0, :] < img_width) & (pts_2d[0, :] >= 0) &
                    (pts_2d[1, :] < img_height) & (pts_2d[1, :] >= 0))[0]
    
    # Pixels, points remained in camera FOV
    pixels_infov = np.around(pts_2d[:, infov].T, decimals=0).astype(int)
    pts_infov = pts[infov]
    return pixels_infov, pts_infov


#cloud = np.array([[[ 9.00108662],[18.61038849],[-2.36147371]],[[ 7.03411068],[18.78492763],[-2.25532085]],[[ 5.06713474],[18.95946677],[-2.149168  ]],[[ 8.82566252],[16.64066466],[-2.3733537 ]],[[ 6.85868657],[16.8152038 ],[-2.26720084]],[[ 4.89171063],[16.98974294],[-2.16104799]],[[ 8.65023841],[14.67094084],[-2.38523369]],[[ 6.68326247],[14.84547998],[-2.27908083]],[[ 4.71628652],[15.02001912],[-2.17292798]],[[ 4.54086242],[13.05029529],[-2.18480797]],[[ 4.36543831],[11.08057147],[-2.19668796]],[[ 6.50783836],[12.87575615],[-2.29096082]],[[ 6.33241425],[10.90603233],[-2.30284081]],[[ 8.4748143 ],[12.70121701],[-2.39711368]],[[ 8.2993902 ],[10.73149319],[-2.40899367]],[[ 8.12396609],[ 8.76176936],[-2.42087366]],[[ 6.15699015],[ 8.9363085 ],[-2.31472081]],[[ 4.1900142 ],[ 9.11084764],[-2.20856795]]]).reshape((-1,3))
#print(cloud)
#proj_mat=np.array([[9.85928103e+02,-9.83854494e+01,-5.74228211e+00,-5.72066751e+01],
#                   [2.56548378e+02,2.51551686e+02,-7.52984508e+02,-1.58003024e+02],
#                   [7.19683045e-01,6.94288944e-01,-4.37916537e-03,-1.04478217e-01]])
#pixels, points=project_2_image(cloud, proj_mat)
#print(pixels)

def project(cloud, case_avp1):
    cloud=np.array(cloud).reshape((-1,3))
    print("To project:",cloud)
    # INF-2/AVP-3
#    proj_mat=np.array([[9.85928103e+02,-9.83854494e+01,-5.74228211e+00,-5.72066751e+01],
#                   [2.56548378e+02,2.51551686e+02,-7.52984508e+02,-1.58003024e+02],
#                   [7.19683045e-01,6.94288944e-01,-4.37916537e-03,-1.04478217e-01]])
    
    
    if case_avp1:
        # INF-1/AVP-1
        proj_mat=np.array([[-7.37348128e+02, -6.79266906e+02,  3.14100062e+01, -6.64150560e+01],
                           [-3.34821269e+01, -3.41687679e+02, -7.71835574e+02, -1.65339315e+02],
                           [ 4.62352393e-02, -9.98529265e-01, -2.83126963e-02, -1.28390817e-01]])
    else:
        # INF-2/AVP-3
        proj_mat=np.array([[9.85928103e+02,-9.83854494e+01,-5.74228211e+00,-5.72066751e+01],
                           [2.56548378e+02,2.51551686e+02,-7.52984508e+02,-1.58003024e+02],
                           [7.19683045e-01,6.94288944e-01,-4.37916537e-03,-1.04478217e-01]])
    
    pixels, points=project_2_image(cloud, proj_mat)
    return pixels