'''
    Python script for merging boundingboxes
'''

import simplejson as json
import string
import re
import sys
import os
import urllib
import numpy as np
from sklearn import mixture
import math
from collections import Counter
import random
import math
import nltk
import shutil


def rm_duplict(fbs, final_info, nrBB_info, rec_info, iname):
    '''im = cv2.imread('orign_imgs/'+iname+'.jpg')
    height, width, depth = im.shape
    linewidth = int(max(height,width)/500)
    for bb in fbs:
        cv2.rectangle(im,(bb[0],bb[1]),(bb[2],bb[3]),(0,0,255),linewidth)
    cv2.imwrite('img/'+iname+'/'+iname+'_tune'+'.jpg', im)'''
    #print '--------test--------'
    #print final_info
    new_fbs = fbs[:]
    new_final_info = final_info#[]
    '''for fi in final_info:
        ct = fi[1]
        this_info = []
        for c in range(ct):
            this_info.append(fi[0])
        new_final_info.append(this_info)'''
    #print new_final_info
    sizes = []
    for f in fbs:
        sizes.append((f[2]-f[0])*(f[3]-f[1]))
    for f in fbs:
        if f not in new_fbs:
            continue
        ind = 0
        for b in new_fbs:
            if b==f:
                ind += 1
                continue
            
            if float(f[2]+f[0])/2>b[0] and float(f[2]+f[0])/2<b[2] and float(f[1]+f[3])/2>b[1] and float(f[1]+f[3])/2<b[3]: #and get_size(f)<get_size(b): #overlap(r1, r2)
                #print 'hi2'
                org_ind = new_fbs.index(f)
                for n in new_final_info[org_ind]:
                    new_final_info[ind].append(n)
                for n in rec_info[org_ind]:
                    rec_info[ind].append(n)
                nrBB_info[ind] += nrBB_info[org_ind]
                del new_final_info[org_ind]
                del nrBB_info[org_ind]
                del rec_info[org_ind]
                new_fbs.remove(f)
                break
            ind += 1
    return new_fbs, new_final_info, nrBB_info, rec_info
def get_size(f):
    return (f[2]-f[0])*(f[3]-f[1])

def rm_outline(positions, info):
    #print positions
    positions = positions.tolist()
    sizes = []
    mids = []
    for p in positions:
        sizes.append((p[2]-p[0])*(p[3]-p[1]))
        mids.append([float(p[2]+p[0])/2, float(p[3]+p[1])/2])
    m = np.mean(sizes)
    s = np.std(sizes)
    
    mids = np.array(mids)
    #print mids
    mids1_m = np.mean(mids[:,0])
    #mids1_m = np.median(mids[:,0])
    mids1_s = np.std(mids[:,0])
    mids2_m = np.mean(mids[:,1])
    #mids2_m = np.median(mids[:,1])
    mids2_s = np.std(mids[:,1])
    
    new_positions = positions
    ind = 0
    for p in positions:
        this_s = (p[2]-p[0])*(p[3]-p[1])
        if math.fabs(this_s - m) > math.sqrt(float(s)):
            new_positions.remove(p)
            #del info[ind]
            ind += 1
            continue
        mid1 = float(p[2]+p[0])/2
        mid2 = float(p[3]+p[1])/2
        if math.fabs(mid1-mids1_m)>float(mids1_s) or math.fabs(mid2-mids2_m)>float(mids2_s):
            new_positions.remove(p)
            #del info[ind]
        ind += 1
            
    return np.array(new_positions), info

def get_major(info):
    #print info
    tups = []
    for i in info:
        tups.append(i[1])
    lst = Counter(tups).most_common()
    highest_count = max([i[1] for i in lst])
    values = [i[0] for i in lst if i[1] == highest_count]
    random.shuffle(values)
    #print tups
    for name in values:
        if len(re.compile('.*identify.*|.*know.*|.*sure.*|.*konw.*|.*poor.*|.*indistinct.*|.*unclear.*|.*none.*|.*fantasy.*|.*sorry.*|.*\?.*|.*clear.*|.*no.*|.*not.*|.*withered.*|.*impossible.*|.*tell.*|.*recognize.*').findall(name))==0:
            #print name
            return [name, highest_count]
    #print 'na'
    return ['na', highest_count]

def entropy2(s):
    p, lns = Counter(s), float(len(s))
    return -sum( count/lns * math.log(count/lns, 2) for count in p.values())

def avg_shapes(shapes_info, m, iname, height, nr_bb_worker, agg_inf, agg_inf2, agg_inf3, gt, pre_k_min=0):
    #print shapes_info
    shapes = []
    info = []
    rec_ind = []
    for s in shapes_info:
        #print s
        shapes.append(s[0:4])
        info.append(s[4:])
        rec_ind.append([s[6],s[4]])
    #print shapes
    #print info
    shapes = np.array(shapes)
    s1, s2 = shapes.shape
    #print s1

    bic_k = 0
    nr = min(10, s1)
    bic_min = sys.maxint
    k_min = sys.maxint
    for k in range(nr):#[pre_k_min, nr]:#
        g = mixture.GMM(n_components=k+1)
        g.fit(shapes)
        bic = g.bic(shapes)
        if bic < bic_min:
            bic_min = bic
            bic_k = k
    #print bic_k
    if pre_k_min>15:
        relax = pre_k_min+3
    else:
        relax = pre_k_min
    k_min = min(s1, max(relax, bic_k))  # !!important pre_k_min+3 is the prior knowledge
        
    print k_min
    nr_bbs = [nr_bb_worker[w] for w in nr_bb_worker]
    k_min_entropy = entropy2(nr_bbs)
    print nr_bbs
    print k_min_entropy
    most_frq_k = Counter(nr_bbs).most_common()[0][0]

    print '----'
    ''' TODO: make entropy item number invariant '''
    if k_min_entropy<1.37:
        k_min = most_frq_k
    
    print k_min
    print '-----------------'
    g = mixture.GMM(n_components=k_min)
    g.fit(shapes)
    clus = g.predict(shapes).tolist()
    
    shapes = shapes.tolist()
    final_boxes = []
    label_info = []
    nrBB_info = []
    rec_info = []
    for i in range(k_min):
        positions = []
        this_info = []
        srec = []
        ind = 0
        for c in clus:
            if c == i:
                positions.append(shapes[ind])
                this_info.append(info[ind])
                srec.append(rec_ind[ind])
            ind += 1
        if len(positions)==0:
            continue
        nrBB_info.append(len(positions))
        positions = np.array(positions)
        #print len(positions)
        positions, this_info2 = rm_outline(positions, this_info)
        #print positions
        #print this_info
        final_boxes.append([int(np.median(positions[:,0])),int(np.median(positions[:,1])),int(np.median(positions[:,2])),int(np.median(positions[:,3]))])
        #print this_info
        label_info.append(get_all(this_info))
        rec_info.append(srec)
        
        #cv2.rectangle(im,(int(np.mean(positions[:,0])),int(np.mean(positions[:,1]))),(int(np.mean(positions[:,2])),int(np.mean(positions[:,3]))),(0,255,0),10)
    final_boxes, label_info, nrBB_info, rec_info = rm_duplict(final_boxes, label_info, nrBB_info, rec_info, iname)
    ind = 0
    '''if os.path.isdir('img_crop/'+iname):
        shutil.rmtree('img_crop/'+iname)
    os.makedirs('img_crop/'+iname)'''
    f = open('img/'+iname+'/'+iname+'_agg_label','w')
    
    for fb in final_boxes:
        ''''h, w, d = im.shape
        cv2.rectangle(im,(fb[0], fb[1]),(fb[2], fb[3]), (0,0,255),int(max(h,w)/500))'''
        #cv2.putText(im,str(ind), (fb[0], int(fb[1]+0.025*height)), cv2.FONT_HERSHEY_SIMPLEX, 2, 255, 10)
        # WRITE THE CROPED IMAGE
        agg_inf3.write(iname+','+str(ind)+','+str(fb[0])+','+str(fb[1])+','+str(fb[2])+','+str(fb[3])+'\n')
        '''write_crop(iname, fb, ind, agg_inf2)'''
        #AGGREGATE LABEL and WRITE
        name = get_major_flat(label_info[ind])
        f.write(str(ind)+': ')
        for n in name:
            if n!=name[-1]:
                f.write(n+',')
            else:
                f.write(n)
        #WRITE SUPPORTING INFORMATION    
        f.write('. \n\tNo.supporting bounding boxes: '+str(nrBB_info[ind])+'\n\tSupporting labels: ')
        cel = set(label_info[ind])
        for c in cel:
            f.write('('+c+','+str(label_info[ind].count(c))+')  ')
        f.write('\n\tSupporting bounding box indices: ')
        dist_worker = []
        nr_bb_this_worker = []
        for rec in rec_info[ind]:
            f.write(str(rec[0])+'_'+str(rec[1])+'  ')
            dist_worker.append(rec[0])
            u = rec[0]
            nr_bb_this_worker.append(nr_bb_worker[u])
        f.write('\n\tNo.distinct supporting workers: '+str(len(set(dist_worker)))+'\n\tAvg.No.flowers by supporting workers: '+str(round(np.mean(nr_bb_this_worker),2)))
        f.write('\n')
        # AGGREGATE INFORMATION AND WRITE TO A SINGLE CSV FILE
        agg_inf.write(iname+','+str(ind)+','+str(nrBB_info[ind])+','+str(len(set(dist_worker)))+','+str(round(float(nrBB_info[ind])/len(set(dist_worker)),2))+','+str(round(np.mean(nr_bb_this_worker),2))+',')
        
        for n in range(len(name)):
            if n!=len(name)-1:
                agg_inf.write(name[n]+'|')
            else:
                agg_inf.write(name[n]+',')
        for n in range(len(label_info[ind])):
            if n!=len(label_info[ind])-1:
                agg_inf.write(label_info[ind][n]+'|')
            else:
                agg_inf.write(label_info[ind][n]+',')
        for rec in range(len(rec_info[ind])):
            if rec != len(rec_info[ind])-1:
                agg_inf.write(str(rec_info[ind][rec][0])+'_'+str(rec_info[ind][rec][1])+'|')
            else:
                agg_inf.write(str(rec_info[ind][rec][0])+'_'+str(rec_info[ind][rec][1])+',')
        if iname in gt:
            for g in range(len(gt[iname])):
                if g != len(gt[iname])-1:
                    agg_inf.write(str(gt[iname][g])+',')
                else:
                    agg_inf.write(str(gt[iname][g])+'\n')
        else:
            agg_inf.write(',,,,,\n')
                    
        ind += 1
    f.close()
    '''cv2.imwrite('img/'+iname+'/'+iname+'_agg.jpg', im)'''
    return final_boxes
    
def write_crop(iname, fb, ind, agg_inf2):
    im_crop = cv2.imread('orign_imgs/'+iname+'.jpg')
    h, w, d = im_crop.shape
    width = fb[2]-fb[0]
    height = fb[3] - fb[1]
    cv2.rectangle(im_crop,(fb[0], fb[1]),(fb[2], fb[3]), (0,0,255),int(max(min(width,height)/600+1, 1)))
    crop_temp = im_crop[max(0,int(fb[1]-float(height)/5)):min(h,int(fb[3]+float(height*1)/5)), max(0,int(fb[0]-float(width)/5)):min(w,int(fb[2]+float(width*1)/5))]
    cv2.imwrite('img_crop/'+iname+'_'+str(ind)+'_crop.jpg', crop_temp)
    flag = True
    cv2.rectangle(im_crop,(fb[0], fb[1]),(fb[2], fb[3]), (0,0,255),int(max(h,w)/500))
    if os.path.exists('img_crop/'+iname+'_'+str(ind)+'_crop.jpg'):
        cv2.imwrite('img_crop/'+iname+'_'+str(ind)+'_full.jpg', im_crop)
    else:
        flag = False
    if os.path.exists('img_crop/'+iname+'_'+str(ind)+'_full.jpg') and os.path.exists('img_crop/'+iname+'_'+str(ind)+'_crop.jpg'):
        agg_inf2.write(iname+','+str(ind)+',http://wisserver.st.ewi.tudelft.nl/wisdata/prints/img_crop/'+iname+'_'+str(ind)+'_full.jpg,http://wisserver.st.ewi.tudelft.nl/wisdata/prints/img_crop/'+iname+'_'+str(ind)+'_crop.jpg\n')
    else:
        flag = False
    if not flag:
        print '.....error: '+iname
        
def get_all(tups):
    rt = []
    for t in tups:
        #print t
        if t[3]=="unable":
            rt.append('na')
            #print 'na'
        elif t[3]=="name":
            if len(re.compile('.*remember.*|.*identify.*|.*know.*|.*sure.*|.*konw.*|.*poor.*|.*indistinct.*|.*unclear.*|.*sorry.*|.*\?.*|.*clear.*|.*no.*|.*not.*|.*withered.*|.*impossible.*|.*tell.*|.*recognize.*').findall(t[1]))==0:
                rt.append(t[1])
                #print t[1]
            else:
                rt.append('other')
                #print 'other'
        else:
            rt.append('fantasy')
            #print 'fantasy'
    return rt

def get_major_flat(tups):
    if len(tups)==0:
        return ['na']

    tups = [y for y in tups if y != 'na']
    #print tups
    if len(tups)==0:
        return ['na']
    lst = Counter(tups).most_common()
    highest_count = max([i[1] for i in lst])
    values = [i[0] for i in lst if i[1] == highest_count]
        
    return values

def get_id(urltext):
    id_regx = re.compile('id=.+')
    ids = id_regx.findall(urltext)
    id = ids[0][3:]
    return id

def get_gt():
    gt = dict([])
    for line in open('groud_truth.csv'):
        fields = line.split(';')
        id = fields[0]
        amount = fields[3]
        prominence = fields[4]
        nrflowers_lower = fields[10]
        nrflowers_upper = fields[11]
        nrtypes_lower = fields[12]
        nrtypes_upper = fields[13]
        gt[id] = [amount, prominence, nrflowers_lower, nrflowers_upper, nrtypes_lower, nrtypes_upper]
        
    return gt
    