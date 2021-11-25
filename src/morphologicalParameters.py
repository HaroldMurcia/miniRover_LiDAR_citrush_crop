# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 13:28:35 2020

@authors: Harold Murcia & Sebastian_Tilaguy
"""
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
import numpy as np
import time
import pandas as pd
from scipy.spatial import distance_matrix
from numpy import genfromtxt
import os, sys, warnings

path=os.path.dirname(os.getcwd())

class hCannopy(object): # Crea clase

    def __init__(self,filename,cx,cy,cz):
        tic = time.time()
        self.filename=filename
        print('=============================================================')
        print(' Universidad de Ibagué - D+TEC - www.haroldmurcia.com\n'+
        ' 3D CROP - alphaVersion [Linux powered] - www.haroldmurcia.com\n')
        print('=============================================================')
        print('Input file = '+self.filename+'\n')
        print('=============================================================\n'+
              '|                        Instructions                       |\n'+
              '-------------------------------------------------------------\n'+
              '|  1. Position the mouse cursor in the center of a tree and |\n'+
              '|     without releasing it, drag the cursor to the outermost|\n'+
              '|     edge of the tree and release.                         |\n'+
              '|                                                           |\n'+
              '|  2. Once done, move the cursor around a bit and a red     |\n'+
              '|     circle will appear around the tree centered on the    |\n'+
              '|     point you initially selected. Move the cursor to the  |\n'+
              '|     next tree and repeat step 1 on all the trees of the   |\n'+
              '|     same groove.                                          |\n'+
              '|                                                           |\n'+
              '|  3. Once you are done with all the trees in the row, press|\n'+
              '|     the "Groove Change" key to start the process with a   |\n'+
              '|     new row, repeat steps 1,2,3 until you mark all the    |\n'+
              '|     trees in the point cloud.                             |\n'+
              '|                                                           |\n'+
              '|  4. Select the menu option "Parameter calculation" that   |\n'+
              '|     you want the software to calculate.                   |\n'+
              '=============================================================\n'+
              '|                        Special keys                       |\n'+
              '-------------------------------------------------------------\n'+
              '|  "c"     : Delete last tree                               |\n'+
              '|  "space" : Groove change                                  |\n'+
              '|  "z"     : Save measurements                              |\n'+
              '|  "f"     : fullscreen or minimize                         |\n'+
              '|  "g"     : Grid on or off                                 |\n'+
              '|  "p"     : Move graph                                     |\n'+
              '|  "s"     : Save graph                                     |\n'+
              '|  "k"     : Maximize x-axis                                |\n'+
              '|  "l"     : Maximize y-axis                                |\n'+
              '|  "Q"     : Quit graph and finish                          |\n'+
              '=============================================================\n'+
              '|                    Parameter estimation                   |\n'+
              '-------------------------------------------------------------\n'+
              '|  "1" : Tree high                                          |\n'+
              '|  "2" : Distance between trees                             |\n'+
              '|  "3" : Distance between grooves                           |\n'+
              '|  "4" : Diameter of canopy                                 |\n'+
              '|  "5" :                                                    |\n'+
              '|  "6" :                                                    |\n'+
              '|  "7" :                                                    |\n'+
              '|  "8" :                                                    |\n'+
              '|  "9" : 3D view of a tree                                  |\n'+
              '-------------------------------------------------------------\n')
        # Design Params
        self.z_ref = 1.00 #given high weeda
        self.cx=cx
        self.cy=cy
        self.cz=cz
        print('txt file is been reading...')
        df = pd.read_csv(self.filename, sep=",", header = 0)
        df.columns = ["X","Y","Z"]
        ##
        df.Z = df.Z - cx*df.X - cy*df.Y - cz
        ##
        self.data = df.drop(df[df['Z']<=self.z_ref].index)
        L = len(self.data)
        print('txt file has been read... file has '+str(L)+' lines')
        print('\t Time used to read file: '+str(time.time()-tic)+' sec')
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        #self.data.plot.scatter(x='X', y='Y',c='Z', ax=self.ax, s=0.5)
        self.ax.plot(self.data.X, self.data.Y,'.')
        self.ax.set_xlim([self.data['X'].min()-5, self.data['X'].max()+5])
        self.ax.set_ylim([self.data['Y'].min()-5, self.data['Y'].max()+5])
        cursor = Cursor(self.ax, horizOn=True,vertOn=True,color='green',linewidth=1.0)
        # Flags
        # Groove params
        self.contG = 0
        self.contT = 0
        self.center = pd.DataFrame([],columns=['Center_x'+str(self.contG), 'Center_y'+str(self.contG), 'radio'+str(self.contG)])
        self.click_x = 0
        self.click_y = 0
        t = [np.linspace(0.0,2.0*np.pi,180)]
        self.Xc = np.sin(t)
        self.Yc = np.cos(t)
        # Measurement params
        self.num = 500
        self.l_Croove = 1
        self.h = []
        self.diameter = []
        self.dt = []
        self.dg = []
        # Main function
        print('\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        print('Begin the interactive platform...')
        self.main()

    def onclick(self,event):
        self.click_x = event.xdata
        self.click_y = event.ydata
        self.p, = plt.plot(self.click_x,self.click_y,'xr')
        self.fig.canvas.mpl_connect('button_release_event',self.offclick)

    def offclick(self,event):
        x2 = event.xdata
        y2 = event.ydata
        self.p, = plt.plot(x2,y2,'xy')
        radio = distance_matrix([[self.click_x, self.click_y]], [[x2, y2]])
        df = pd.DataFrame({'Center_x'+str(self.contG): [self.click_x],
                           'Center_y'+str(self.contG): [self.click_y],
                           'radio'+str(self.contG): radio[0]},
                          index=[self.contT])
        self.center = self.center.append(df)

        Xc_k = radio[0][0]*self.Xc[0,] + self.click_x
        Yc_k = radio[0][0]*self.Yc[0,] + self.click_y
        self.p, = plt.plot(Xc_k,Yc_k,'r')
        # print(self.center.loc[self.contT])
        self.contT = self.contT + 1

    def onKey(self,event):
        if (event.key==' '):
            self.contG = self.contG + 1
            df = pd.DataFrame([],columns=['Center_x'+str(self.contG), 'Center_y'+str(self.contG), 'radio'+str(self.contG)])
            self.center = pd.concat([self.center, df], axis=1)
            self.contT = 0
            print('change of groove')
        elif (event.key=='c'):
            pass
        elif (event.key=='z'):
            try:
                print("Saving data:", path+"/data/Processed_data.csv")
            except:
                pass
            self.h = np.array(self.h)
            self.dt = np.array(self.dt)
            self.dg = np.array(self.dg)
            maxi = max([len(self.h), len(self.dt), len(self.dg)])
            self.h  = np.append(self.h , np.zeros([1,np.abs(maxi-len(self.h))]) )
            self.dt = np.append(self.dt, np.zeros([1,np.abs(maxi-len(self.dt))]) )
            self.dg = np.append(self.dg, np.zeros([1,np.abs(maxi-len(self.dg))]) )
            df = pd.DataFrame({'high': self.h,'D_tree': self.dt,'D_groove': self.dg,'Diameter': self.diameter})
            df.to_csv(path+"/data/Processed_data_alphaRover.csv",index=False,sep=",")
        elif (event.key=='0'):
            pass
        elif (event.key=='1'):
            self.h_meassure(self.center)
        elif (event.key=='2'):
            self.D_tree(self.center)
        elif (event.key=='3'):
            self.D_Grooves(self.center)
        elif (event.key=='4'):
            self.Diameter(self.center)
        elif (event.key=='5'):
            pass
        elif (event.key=='6'):
            pass
        elif (event.key=='7'):
            pass
        elif (event.key=='8'):
            pass
        elif (event.key=='9'):
            pass
        elif (event.key=='q'):
            exit()
        else:
            print('Unkown key')

    def h_meassure(self,df):
        tic = time.time()
        N = (self.contG)+1
        k = 0
        # print(df)
        print('Height data')
        for i in range(0,N):
            croop = df[['Center_x'+str(i), 'Center_y'+str(i), 'radio'+str(i)]].dropna(axis=0)
            croop = croop.rename(columns={'Center_x'+str(i): "Xc", 'Center_y'+str(i): "Yc", 'radio'+str(i): "r"})
            # print(croop['r'])
            for j in croop.index:
                x_max = croop['Xc'][j] + croop['r'][j]
                x_min = croop['Xc'][j] - croop['r'][j]
                y_max = croop['Yc'][j] + croop['r'][j]
                y_min = croop['Yc'][j] - croop['r'][j]
                # print(x_max, x_min, y_max, y_min)
                points = self.data.drop(self.data[self.data['X']<x_min].index)
                points = points.drop(points[points['X']>x_max].index)
                points = points.drop(points[points['Y']<y_min].index)
                points = points.drop(points[points['Y']>y_max].index)
                # print(points)
                b = np.matrix([[croop['Xc'][j]],[croop['Yc'][j]]]).T
                # print(b)
                # print(b.shape)
                a = np.append(np.matrix(points['X'].to_numpy()).T,
                              np.matrix(points['Y'].to_numpy()).T,1)
                # print(a)
                for cont in range(int(len(a)/self.num + 1)):
                    n1 = self.num*cont
                    n2 = (self.num)+self.num*cont
                    c = np.matrix(a[n1:n2,:])
                    c = np.append(c,b,0)
                    c = distance_matrix(c, c)
                    c = c[:][-1]
                    c = np.matrix(c[0:len(c)-1])
                    if cont==0:
                        distance = c
                    else:
                        distance = np.append(distance,c,axis=1)
                    # print(distance.shape)
                distance = np.matrix(distance)
                # print(distance)
                distances = pd.DataFrame(distance.T,
                                         columns={'rp'},
                                         index=points.index)
                del distance
                # print(distances)
                points = points.drop(distances[distances['rp']>croop['r'][j]].index)
                del b
                del a
                del distances
                if (i==0)and(j==0):
                    tree = pd.DataFrame(points[['X','Y','Z']].values)
                else:
                    tree = pd.concat([tree,
                                      pd.DataFrame(points[['X','Y','Z']].values,)],
                                     ignore_index=True, axis=1)
                Np_per_tree = len(tree.index)
                z_max = tree[k+2].max()
                # outliers
                # Método distancia IQR
                Q1 = tree[k+2].quantile(0.25)
                Q3 = tree[k+2].quantile(0.75)
                # Calculating “IQR”
                IQR = Q3 - Q1
                # Calculating lower and upper whiskers
                upper = Q3 + 1.5*IQR
                lower = Q1-1.5*IQR
                inliers = tree[k+2][(tree[k+2] < upper) | (tree[k+2] > lower)]
                #
                ground_plane = tree[k+0].mean()*self.cx + tree[k+1].mean()*self.cy + self.cz
                h = round(z_max - ground_plane,4)
                print('=============================================================\n'+
                      '|  Tree No. '+str(j)+', groove No. '+str(i)+'\n'+
                      '-------------------------------------------------------------\n'+
                      '|  Canopy height = '+str(inliers.max())+' mts \n'+
                      '|  Point numbers per tree = '+str(Np_per_tree)+'\n'+
                      '|  Processing time = '+str(time.time()-tic)+' seg')
                self.p, = plt.plot(tree.loc[:,k],tree.loc[:,k+1],'.g')
                self.h.append(inliers.max())
                k = k + 3
        # print(tree)

    def Diameter(self,df):
        tic = time.time()
        N = (self.contG)+1
        # print(df)
        print('Diameter')
        for i in range(0,N):
            croop = df[['Center_x'+str(i), 'Center_y'+str(i), 'radio'+str(i)]].dropna(axis=0)
            croop = croop.rename(columns={'Center_x'+str(i): "Xc", 'Center_y'+str(i): "Yc", 'radio'+str(i): "r"})
            # print(croop['r'])
            for j in croop.index:
                x_max = croop['Xc'][j] + croop['r'][j]
                x_min = croop['Xc'][j] - croop['r'][j]
                y_max = croop['Yc'][j] + croop['r'][j]
                y_min = croop['Yc'][j] - croop['r'][j]
                # print(x_max, x_min, y_max, y_min)
                points = self.data.drop(self.data[self.data['X']<x_min].index)
                points = points.drop(points[points['X']>x_max].index)
                points = points.drop(points[points['Y']<y_min].index)
                points = points.drop(points[points['Y']>y_max].index)
                # print(points)
                b = np.matrix([[croop['Xc'][j]],[croop['Yc'][j]]]).T
                # print(b)
                # print(b.shape)
                a = np.append(np.matrix(points['X'].to_numpy()).T,
                              np.matrix(points['Y'].to_numpy()).T,1)
                # print(a)
                for cont in range(int(len(a)/self.num + 1)):
                    n1 = self.num*cont
                    n2 = (self.num)+self.num*cont
                    c = np.matrix(a[n1:n2,:])
                    # print(c)
                    c = np.append(c,b,0)
                    # print(c)
                    c = distance_matrix(c, c)
                    # print(c)
                    c = c[:][-1]
                    # print(c)
                    c = np.matrix(c[0:len(c)-1])
                    if cont==0:
                        distance = c
                    else:
                        distance = np.append(distance,c,axis=1)
                    # print(distance.shape)
                    # print(type(distance))
                distance = np.matrix(distance)
                # print(distance)
                distances = pd.DataFrame(distance.T,
                                         columns={'rp'},
                                         index=points.index)
                del distance
                del b
                del a
                # print(distances)
                points = points.drop(distances[distances['rp']>croop['r'][j]].index)
                distances = distances.drop(distances[distances['rp']>croop['r'][j]].index)
                # print(points)
                maximo = distances['rp'].max()
                # print(maximo)
                indice = distances.loc[distances['rp'] == maximo].index
                # print(indice)
                # print(points.loc[indice,['X','Y']])
                d = 2*distances.loc[indice,'rp']
                # print(d.values)
                print('=============================================================\n'+
                      '|  Tree No. '+str(j)+', groove No. '+str(i)+'\n'+
                      '-------------------------------------------------------------\n'+
                      '|  Diameter = '+str(d.values)+' mts \n'+
                      '|  Processing time = '+str(time.time()-tic)+' seg')
                self.p, = plt.plot(points.loc[indice,'X'],points.loc[indice,'Y'],'.c')
                self.diameter.append(d.values[0])



    def D_tree(self,df):
        tic = time.time()
        N = (self.contG)+1
        print('Distance between trees:')
        # print(df)
        for i in range(0,N):
            croop = df[['Center_x'+str(i), 'Center_y'+str(i)]].dropna(axis=0)
            # print(croop)
            # print(len(croop))
            if (len(croop)>1):
                a = np.matrix([croop['Center_x'+str(i)],croop['Center_y'+str(i)]]).T
                # print(a)
                # print(a.shape)
                distance = []
                for cont in range(int(len(a)/self.num + 1)):
                    n1 = self.num*cont
                    n2 = (self.num)+self.num*cont
                    c = np.matrix(a[n1:n2,:])
                    b = distance_matrix(c, c)
                    print('=============================================================\n'+
                          '|  Distance between trees in groove No. '+str(i)+'\n'+
                          '-------------------------------------------------------------')
                    for j in range(len(a)-1):
                        distance = np.append(distance,b[j][j+1])
                        # print(b[j][j+1])
                        print('|  Tree No. '+str(j)+' to tree No. '+str(j+1)+'\n'+
                              '|       Distance = '+str(b[j][j+1])+' mts \n'+
                              '-------------------------------------------------------------')
                        self.p, = plt.plot([c[j,0],c[j+1,0]],[c[j,1],c[j+1,1]],'--r')
                        self.dt.append(b[j][j+1])
                d_avg = np.average(distance)
                print('|  Average distance per groove = '+str(d_avg)+' mts \n'+
                      '|  Processing time = '+str(time.time()-tic)+' seg')
            else:
                print('It is necessary to mark more than one tree for this option.')

    def D_Grooves(self,df):
        tic = time.time()
        N = (self.contG)+1
        print('Distance between grooves:')
        # print(df)
        x_lim = np.array(self.ax.get_xlim())
        x_line = np.linspace(x_lim[0],x_lim[1],100)
        xo = ((x_lim[1] - x_lim[0])/2.0) + x_lim[0]
        pol_1 = []
        distance = []
        for i in range(0,N):
            croop = df[['Center_x'+str(i), 'Center_y'+str(i)]].dropna(axis=0)
            x = np.array(croop['Center_x'+str(i)])
            y = np.array(croop['Center_y'+str(i)])
            if (i==0):
                self.l_Croove=len(croop)
            if (len(croop)>1)and(self.l_Croove>1):
                pol = np.polyfit(x,y,1)
                if (i==0):
                    points = np.array([[x_lim[0], pol[0]*x_lim[0]+pol[1]],
                                       [x_lim[1], pol[0]*x_lim[1]+pol[1]]])
                else:
                    points = np.append(points,
                                       np.array([[x_lim[0], pol[0]*x_lim[0]+pol[1]],
                                                 [x_lim[1], pol[0]*x_lim[-1]+pol[1]]]),
                                       axis=0)
                    c = np.matrix(points[-4:,:])
                    b = distance_matrix(c, c)
                    distance = np.append(distance,
                                         (b[2][0] + b[3][1])/2.0)
                    ms = -1.0/pol_1[0]
                    a_s = (pol_1[0]-ms)*xo+pol_1[1]
                    # s = ms*x_line+a_s
                    x_ = (a_s-pol[1])/(pol[0]-ms)
                    self.p, = plt.plot([x_, xo],
                                       [pol[0]*x_+pol[1], pol_1[0]*xo+pol_1[1]],
                                       '--g')
                r = pol[0]*x_line+pol[1]
                self.p, = plt.plot(x_line,r,'.k')
                pol_1 = pol
            elif(len(croop)==1)and(self.l_Croove==1):
                if (i==0):
                    points = np.array([[x[0], y[0]]])
                else:
                    points = np.append(points,
                                       np.array([[x[0], y[0]]]),
                                       axis=0)
                    b = distance_matrix(points, points)
                    distance = np.append(distance,
                                         b[i][i-1])
                    x_g = np.array(points[i-1:i+1,0])
                    y_g = np.array(points[i-1:i+1,1])
                    self.p, = plt.plot(x_g,y_g,'--g')
            else:
                raise Exception('In one groove there is just a tree and the others there are more than one. If desired, you can work with a single tree PER row or use more than one tree in ALL rows to improve accuracy.')
            if (i>0):
                print('=============================================================\n'+
                      '|  Distance between grooves No.'+str(i-1)+' and '+str(i)+'\n'+
                      '-------------------------------------------------------------\n'+
                      '|  Distance = '+str(distance[i-1])+' mts')
                self.dg.append(distance[i-1])
            self.l_Croove = len(croop)
        d_avg = np.average(distance)
        print('|  Average distance = '+str(d_avg)+' mts \n'+
              '|  Processing time = '+str(time.time()-tic)+' seg')


    def main(self):
        warnings.filterwarnings("ignore")
        self.fig.canvas.mpl_connect('button_press_event',self.onclick)
        self.fig.canvas.mpl_connect('key_press_event',self.onKey)
        self.ax.set_ylabel('y\n[mts]')
        self.ax.set_xlabel('x\n[mts]')
        self.ax.figure.set_size_inches(15, 15)
        self.ax.set_aspect('equal', 'box')
        plt.show()

if __name__ == '__main__':
    os.system('clear')
    filename = sys.argv[1]
    plane = genfromtxt(path+"/data/plane_measured_coef.csv", delimiter=',')
    cv = hCannopy(filename,plane[0],plane[1],plane[2])
