import string
import psycopg2
from scipy.stats.stats import pearsonr
from scipy.stats.stats import spearmanr
import numpy
import matplotlib.pyplot as plt
import pylab
import sys
import os
import math
from scipy import linalg

import scipy
import pylab
import scipy.cluster.hierarchy as sch

sys.path.append('/usr/local/Cellar/opencv/2.4.8.2/lib/python2.7/site-packages')
import cv2
import urllib
image = urllib.URLopener()

#################################### main function ##############################

def test_img():
    im = cv2.imread('test.jpg')
    imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(imgray,127,255,0)
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cnt = contours[0]
    cv2.drawContours(im,[cnt],-1,(255,0,0),3)
    x,y,w,h = cv2.boundingRect(cnt)
    print x
    cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)
    crop_img = im[int(y-float(h)/5):int(y+float(6*h)/5), int(x-float(w)/5):int(x+float(6*w)/5)]
    cv2.imwrite('test.png', crop_img)
def test_result():
    nr = 0
    full_nr = 0
    crop_nr = 0
    for line in open('img_crop/info2.csv'):
        nr += 1
        if nr==1:
            continue
        fields = line.split(',')
        img_full = 'img_crop/'+fields[0]+'_'+str(fields[1])+'_full.jpg'
        img_crop = 'img_crop/'+fields[0]+'_'+str(fields[1])+'_crop.jpg'
        if not os.path.exists(img_full) or not os.path.exists(img_crop):
            print fields[0]
        if os.path.exists(img_full):
            full_nr += 1
        if  os.path.exists(img_crop):
            crop_nr += 1
    print full_nr
    print crop_nr
    print nr-1
    return 0
def test_result2():
    nr = 0
    full_nr = 0
    crop_nr = 0
    for line in open('img_crop/data_info.csv'):
        nr += 1
        if nr==1:
            continue
        fields = line.split(',')
        img_full = 'http://wisserver.st.ewi.tudelft.nl/wisdata/prints/img_crop/'+fields[0]+'_'+str(fields[1])+'_full.jpg'
        img_crop = 'http://wisserver.st.ewi.tudelft.nl/wisdata/prints/img_crop/'+fields[0]+'_'+str(fields[1])+'_crop.jpg'
        image.retrieve(img_full, 'img_test/'+fields[0]+'_'+str(fields[1])+'_full.jpg')
        image.retrieve(img_crop, 'img_test/'+fields[0]+'_'+str(fields[1])+'_crop.jpg')
        
    print nr-1
    return 0

def test_result3():
    nr = 0
    full = dict([])
    crop = dict([])
    for line in open('img_crop/data_info.csv'):
        nr += 1
        if nr==1:
            continue
        fields = line.split(',')
        img_full = fields[0]+'_'+str(fields[1])+'_full.jpg'
        img_crop = fields[0]+'_'+str(fields[1])+'_crop.jpg'
        if img_full in full:
            print img_full
        else:
            full[img_full] = 1
        if img_crop in crop:
            print img_crop
        else:
            crop[img_crop] = 1
        
    print nr-1
    return 0
if __name__ == '__main__':
    test_result3()
