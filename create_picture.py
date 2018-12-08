#coding:utf-8
import os
import cv2
import numpy as np

def hand(name):
    num=name
    name=str(name)
    i=0
    while True:
        if num>0:
            i=i+1
            num=int(num/10)
        else:
            break
    for j in range(5-i):
        name='0'+name
    return name
videoCapture = cv2.VideoCapture('WIN_20180412_16_46_21_Pro.mp4')
#获得码率及尺寸
fps = videoCapture.get(cv2.CAP_PROP_FPS)
size = (int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)))

#读帧
if not os.path.exists('original_slam/'):
    os.makedirs('original_slam')
success, frame = videoCapture.read()
idx = 1
while success:
    success, frame = videoCapture.read() #获取下一帧
    cv2.imshow("显示", frame) #显示
    name=hand(idx)
    cv2.imwrite('original_slam/'+name+'.png',frame)
    idx = idx + 1
    cv2.waitKey(int(fps)) #延迟
videoCapture.release()