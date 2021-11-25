# miniRover on citrush crop

This repository contains code implementations related to the development of a low-cost mobile platform and its use for 3D crop mapping.

The follo youtube video shows the data collection experiment with a terrestrial robotic platform and a 2D Hokuyo LiDAR into a citrus crop in Tolima Colombia:

[![Video into the crop](https://github.com/HaroldMurcia/test/blob/master/media/alpha_view.png)](https://youtu.be/J0KDFF0y5h0)

## Data visualisation
Download the data cloud of interest in LAS format and upload it to the website [https://plas.io/](https://plas.io/)
 * [Tree](https://drive.google.com/file/d/1jHU7twbM_ORyjtLndBJXQhoLzjXEDz7I/view?usp=sharing)
 * [20 Trees Point Cloud](https://drive.google.com/file/d/1mD_8spnglTPJNqIVPYlsTTdr861dIjRh/view?usp=sharing)
 * [12 Trees Point Cloud](https://drive.google.com/file/d/1o5JJlDWtBlff8iKg46ag7s3j59gyD_Ft/view?usp=sharing)

![LiDAR_view](/media/visualization.gif)

## Hardware requirements
This work was carried out with the use of an unmanned ground vehicle developed in the general framework of our project.
The details of our platform called alphaRover can be found in the following repository: https://github.com/HaroldMurcia/AlphaROVER

The UGV has a 2D sensor on board that captures a profile of the cangecation environment at a 45-degree angle to the ground.
![LiDAR_view](/media/laserScan_view.gif)

The mode of operation is offline, in the field the platform makes a route in which it acquires data in a rosbag format. At the end, the data is downloaded and processed with an algorithm that converts the data into a TXT file (details in the following repository: https://github.com/HaroldMurcia/alphaROVER-raw2LAS) which is then transformed into LAS with the [LAS2TXT](https://github.com/HaroldMurcia/alphaROVER-raw2LAS) tool of the [LASTools](https://rapidlasso.com/lastools/) software.

## Software requirements
This project is powered by Linux and an [Ubuntu 20.04](https://ubuntu.com/download/desktop) operating system was used for data processing. The visualisation of the point clouds can be done in LAS or TXT format, for which an online visualisation website [PLAS](www.plas.io) and the free software [CloudCompare](https://www.cloudcompare.org/main.html) were used.

The algorithms were implemented in Python 3 and made use of the following additional libraries:
* pandas
* scipy
* warnings
* sklearn

## Data Downloading >>> repository

Download the data and add it to the following path: ```<~YOUR-REPO/data>```

* [miniRover PointCloud txt](https://drive.google.com/file/d/1e1cbKYAsOmccj7Haoo4NENBRZAqjRw8n/view?usp=sharing)
* [Ground plane points alphaRover](https://drive.google.com/file/d/13RYVPbT3c3-8hP4tXwiQ1WmkufMZOzbP/view?usp=sharing)
* [Ground plane coefficients alphaRover](https://drive.google.com/file/d/1zVbuu55M49Hda2r26XUe2CPTCRF0RXjS/view?usp=sharing)
* [Reference values](https://drive.google.com/file/d/1Hs52cXRwoU9emo4JHETrO4oHEOZIld8p/view?usp=sharing)
* [Measurements obtained from the miniRover's point cloud](https://drive.google.com/file/d/1civKaTYtRBYCa_ZEFj-SIbOKzFa6IzFX/view?usp=sharing)

## How to run?

access the /src folder of the repository from the Linux console and then run the following instructions.

```console
python3 morphologicalParameters.py ../data/laser_alphaRover_12_paper.txt
```
##### _Table 1. Special key to use the software._
|Character|Function		  | |Number|Parameter estimation|
|-------|-----------------|-|---|---------------|
|_space_|Groove change	  | |_0_||
|_z_|Save measurements	  | |_1_|Tree high|
|_f_|Fullscreen/Minimize  | |_2_|Distance between trees|
|_g_|Grid on/off		  | |_3_|Distance between grooves|
|_p_|Move graph			  | |_4_|Diameter of canopy|
|_s_|Save graph			  | |_5_| |
|_k_|Maximize x-axis	  | |_6_||
|_l_|Maximize y-axis	  | |_7_||
|_q_|Quit graph and finish| |_8_||
||						  | |_9_||

```text
The section of each tree is done manually. Using the mouse the user have to put the cursor on center of the tree that want mark. With left-click holding, move the cursor to outer point of tree. A red _x_ will be appear in center marked and yellow _x_ in the outer point , also will be printed a red circle around selected zone center on red _x_.
```

As the instructions suggest, click on the center of each tree and hold it up to the outer edge of the groove to mark the center of the tree and the suggested radius. This process is repeated until the line of trees is completed, to move to another groove press on the figure the 'space' key and repeat the process. To finish, press the '1', '2', '3' and '4' keys to obtain the measurements, the 's' key to save the image the 'z' key to save the records of the measurements obtained and 'q' key to exit.
![LiDAR_view](/media/process.gif)

Finally, to validate y calculate the error parameters $RMSE and R^2$, the following instruction is executed.

```console
python3 ErrorCalculation.py
```

![Alt text](/media/results.png?raw=true "Results answer")

<hr />

## Authors
Universidad de Ibagué  
[Harold MURCIA](www.haroldmurcia.com)  
Sebastian TILAGUY
