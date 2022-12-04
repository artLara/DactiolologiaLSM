import cv2
import numpy as np
import os

dir_path = '/home/lara/Desktop/DactiolologiaLSM/'
frameSize = (640, 480)

landmarks = ''
velocidad = 'rapido'
name = 'el_columpio_verde_'+velocidad
out = cv2.VideoWriter(dir_path+name+landmarks+'.mp4',cv2.VideoWriter_fourcc(*'MP4V'), 10, frameSize)
dirVideoName = 'video/'
for i in range(len(os.listdir(dir_path+dirVideoName))):
    img = cv2.imread(dir_path+dirVideoName+'frame'+str(i)+'.jpg')
    out.write(img)
out.release()

landmarks = '_landmarks'
out = cv2.VideoWriter(dir_path+name+landmarks+'.mp4',cv2.VideoWriter_fourcc(*'MP4V'), 10, frameSize)
dirVideoName = 'videoLandMarks/'
for i in range(len(os.listdir(dir_path+dirVideoName))):
    img = cv2.imread(dir_path+dirVideoName+'frame'+str(i)+'.jpg')
    out.write(img)
out.release()
