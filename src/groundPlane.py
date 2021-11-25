"""
Created on Wed Jun 17 13:28:35 2020

@authors: Harold Murcia & Sebastian_Tilaguy
"""
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pandas as pd
import os, sys, warnings
from scipy.linalg import lstsq

path=os.path.dirname(os.getcwd())

print('Universidad de Ibagué - D+TEC - www.haroldmurcia.com\n'+
'3D CROP - alphaVersion [Linux powered]\n')

if __name__ == '__main__':
    mode=input("Plesase press 1 if input data is from LiDAR, or 2 if input data is from groundTruth: ")
    if float(mode)==1:
        df = pd.read_csv(path+"/data/alpharover_ground_points.txt")
    else:
        df = pd.read_csv(path+"/data/groundtruth_ground_points.txt")
    N=len(df)
    A=np.ones([N,3])
    B=np.zeros([N,1])
    A[:,0]=df.X.values
    A[:,1]=df.Y.values
    B[:,0]=df.Z.values
    A=np.matrix(A)
    # Manual solution
    fit = (A.T * A).I * A.T * B
    errors = B - A * fit
    residual = np.linalg.norm(errors)
    print("solution: %f x + %f y + %f = z" % (fit[0], fit[1], fit[2]))
    print("errors: \n", errors)
    print("residual:", residual)
    #
    if float(mode)==1:
        np.savetxt(path+"/data/plane_measured_coef.csv", fit.T, delimiter=",")
    else:
        np.savetxt(path+"/data/plane_groundTruth_coef.csv", fit.T, delimiter=",")
