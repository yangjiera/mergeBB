from avg_bb2 import *
import csv
import cv2
import urllib
image = urllib.URLopener()
sys.path.append('/usr/local/Cellar/opencv/2.4.8.2/lib/python2.7/site-packages')

def single_img_avgbb(img_name, gt, agg_inf, agg_inf2, agg_inf3, inputfile):
    if not os.path.isdir('img/'+img_name):
        os.makedirs('img/'+img_name)
    if not os.path.isfile('orign_imgs/'+img_name+'.jpg'):
        image.retrieve('https://www.rijksmuseum.nl/assetimage2.jsp?id='+img_name, 'img/'+img_name+'/'+img_name+'.jpg')
    im = cv2.imread('orign_imgs/'+img_name+'.jpg')
    height, width, depth = im.shape
    linewidth = int(max(height,width)/500)
    
    with open(inputfile, 'rb') as csvfile:
        contentreader = csv.reader(csvfile, delimiter=',')
        no = 0
            
        workers = []
        workers_bbs = dict([])
            
        for line in contentreader:
            no += 1
            if no == 1:
                continue
            else:
                img_name_tmp = line[3]
                iname = get_id(img_name_tmp) 
                if iname == img_name and line[2] not in workers:
                    workers.append(line[2])
                    workers_bbs[line[2]] = []
                    #cv2.putText(im,str(nr_anno), (int(shape['x']*width),int((shape['y']+0.025)*height)), cv2.FONT_HERSHEY_SIMPLEX, 2, 255, 10)                            
                    nr_anno = line[0]
                    workers_bbs[line[2]].append([int(float(line[5])*width),int(float(line[6])*height),int(float(line[5])*width)+int(float(line[7])*width),int(float(line[6])*height)+int(float(line[8])*height), nr_anno, line[4].lower(), line[2], line[9]])
                elif iname == img_name and line[2] in workers:
                    nr_anno = line[0]
                    workers_bbs[line[2]].append([int(float(line[5])*width),int(float(line[6])*height),int(float(line[5])*width)+int(float(line[7])*width),int(float(line[6])*height)+int(float(line[8])*height), nr_anno, line[4].lower(), line[2], line[9]])

    sizes = []
    shapes = []
    k = 0
    k_min = 0
    nr_bb_worker = dict([])
    for w in workers:
        for bb in workers_bbs[w]:
            sizes.append((bb[2]-bb[0])*(bb[3]-bb[1]))
    wi = 0
    for w in workers_bbs:
        #print workers_bbs[w]
        flag = True
        for bb in workers_bbs[w]:
            this_size = (bb[2]-bb[0])*(bb[3]-bb[1])
            if this_size - np.mean(sizes) > 3*np.std(sizes):
                flag = False
        #flag = True # For ground truth, we do not filter any users
        if not flag:
            continue
                
        f = open('img/'+img_name+'/'+img_name+'_'+w+'_label', 'w')
                
        im2 = cv2.imread('orign_imgs/'+img_name+'.jpg')
        for bb in workers_bbs[w]:
            cv2.rectangle(im,(bb[0],bb[1]),(bb[2],bb[3]),(0,0,255),linewidth)
            cv2.rectangle(im2,(bb[0],bb[1]),(bb[2],bb[3]),(0,0,255),linewidth)
            cv2.putText(im2,str(bb[4]), (bb[0],bb[1]), cv2.FONT_HERSHEY_SIMPLEX, 2, 255, 10)
            shapes.append(bb)
            f.write(str(bb[4])+': '+bb[5]+'\n')
        cv2.imwrite('img/'+img_name+'/'+img_name+'_'+w+'.jpg', im2)
        nr_bb_worker[w] = len(workers_bbs[w])
        if len(workers_bbs[w])>k_min:
            k_min = len(workers_bbs[w])
        f.close()
        
    cv2.imwrite('img/'+img_name+'/'+img_name+'_all'+'.jpg', im)
    im = cv2.imread('orign_imgs/'+img_name+'.jpg')
    print shapes
    avged_sp = avg_shapes(shapes, im, 0, img_name, height, nr_bb_worker, agg_inf, agg_inf2, agg_inf3, gt, k_min)
    
def mergeBB(inputfile):
    gt = get_gt()
    
    agg_inf = open('img/support_info.csv', 'w')
    agg_inf.write('image id, bb.index, No.suppt.bb, No.dist.supp.worker, No.avg.supp.bb.perWoker, No.avg.bb.perWorker, agg.lable, supp.bb.labels, supp.bb.indice,'+ 
                  'amount, prominence, nrflower_lower, nrflower_upper, nrtype_lower, nrtype_upper\n')
    agg_inf2 = open('img/data_info.csv', 'w')
    agg_inf2.write('image_id,boundingbox_id,full_url,crop_url\n')
    
    agg_inf3 = open('img/aggBB_info.csv', 'w')
    agg_inf3.write('image_id,boundingbox_id,x1,y1,x2,y2\n')
    
    imgnames = []
    with open(inputfile, 'rb') as csvfile:
        contentreader = csv.reader(csvfile, delimiter=',')
        no = 0
            
        workers = []
        workers_bbs = dict([])
            
        for line in contentreader:
            no += 1
            if no == 1:
                continue
            else:
                temp_img = get_id(line[3])
                if temp_img not in imgnames:
                    imgnames.append(temp_img)
    #imgnames = ['RP-P-1878-A-1872X']
    for img_name in imgnames:
        print img_name
        single_img_avgbb(img_name, gt, agg_inf, agg_inf2, agg_inf3, inputfile)
        
    return img_name