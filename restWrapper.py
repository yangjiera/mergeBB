import json
import csv
from avg_bb2 import get_id
import cv2

def wrapBB(BBs):
    iname = get_id(BBs[0]['src'])
    
    bid = 1
    bbinfo = dict([])
    f = open('server_file/'+iname+'.csv', 'w')
    f.write('''"boxID","taskID","workerID","printID","text","x","y","width","height","type","certainty"\n''')
    for b in BBs:
        #b = json.loads(json.dumps(b, ensure_ascii=False).encode('utf8'))
        #print b
        wid = b['workerID']
        src = b['src']
        text = b['text']
        x = b['shapes'][0]['geometry']['x']
        y = b['shapes'][0]['geometry']['y']
        width = b['shapes'][0]['geometry']['width']
        height = b['shapes'][0]['geometry']['height']
        type = b['type']
        certainty = b['certainty']
        
        f.write(str(bid)+',na,'+str(wid)+','+src+','+text+','+str(x)+','+str(y)+','+str(width)+','+str(height)+','+type+','+certainty+'\n')
        bbinfo[bid] = b
        bid += 1
    f.close()

    s = 'server_file/'+iname+'.csv'
    return s.decode('utf8').encode('ascii', 'replace'), bbinfo

def wrapABB(iname, bb_info):
    coordinates = 'img/aggBB_info.csv'
    supports = 'img/support_info.csv'
    aBB = []
    
    im = cv2.imread('orign_imgs/'+iname+'.jpg')
    height, width, depth = im.shape
    
    with open(supports, 'rb') as csvfile:
        contentreader = csv.reader(csvfile, delimiter=',')
        no = 0
            
        bb = dict([])
            
        for line in contentreader:
            no += 1
            if no == 1:
                continue
            
            ''' GET BASIC INFORMATION FOR AGGREGATED BB'''
            bb['image'] = line[0]
            bb['BBId'] = line[1]
            bb['NoSuppBB'] = line[2]
            bb['NoDistinctSuppWorker'] = line[3]
            bb['AvgSuppBBperWorker'] = line[4]
            bb['AvgBBperWorker'] = line[5]
            
            with open(coordinates, 'rb') as csvfile2:
                contentreader2 = csv.reader(csvfile2, delimiter=',')
                no2 = 0
                    
                shapes = []
                
                ''' GET COORDINATES FOR AGGREGATED BB'''
                for line2 in contentreader2:
                    no2 += 1
                    if no2 == 1:
                        continue
                    if line2[0]!=line[0] or line2[1]!=line[1]:
                        continue
                    shape = dict([])
                    shape['type'] = "rect"
                    shape['geometry'] = dict([])
                    shape['geometry']['x'] = float(int(line2[2]))/width
                    shape['geometry']['y'] = float(int(line2[3]))/height
                    shape['geometry']['width'] = float(int(line2[4])-int(line2[2]))/width
                    shape['geometry']['height'] = float(int(line2[5])-int(line2[3]))/height
                    shapes.append(shape)
                    bb['shapes'] = shapes
                    
            ''' GET SUPPORTING BOUNDING BOXES FOR AGGREGATED BB'''
            supportBid = []
            spbids = line[8].split('|')
            for spbid in spbids:
                spb = spbid.split('_')[1]
                print spb
                supportBid.append(bb_info[int(spb)])
            bb['SuppBBs'] = supportBid
                    
            aBB.append(bb)
            
    return json.dumps([b for b in aBB])