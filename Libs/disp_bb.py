import simplejson as json
import string
import re
import sys
import urllib
image = urllib.URLopener()
sys.path.append('/usr/local/Cellar/opencv/2.4.8.2/lib/python2.7/site-packages')
import cv2


def dispbb():
    f = open('f407055_2.csv')
    no = 0
    k = 0
    for line in f:
        no += 1
        if no == 1:
            continue
        fields = line.split(';')
        if len(fields)<16:
            continue
        ant = fields[15]
        if len(ant) == 0 or ant == '[]':
            continue
        ant = string.replace(ant, '""', '"')[1:-1]
        ant = ant.decode("utf-8")
        ant = json.loads(ant)
        print ant[0]['src']
        image.retrieve(ant[0]['src'], 'img/'+str(k)+'.jpg')
        im = cv2.imread('img/'+str(k)+'.jpg')
        height, width, depth = im.shape
        for a in ant:
            shape = a['shapes'][0]['geometry']
            cv2.rectangle(im,(int(shape['x']*width),int(shape['y']*height)),(int(shape['x']*width)+int(shape['width']*width),int(shape['y']*height)+int(shape['height']*height)),(0,255,0),10)
        #cv2.imshow('Features', im)
        cv2.imwrite('img/'+str(k)+'.jpg', im)
        k += 1
    print k

if __name__ == '__main__':
    dispbb()    