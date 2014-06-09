import string
import json
import re

def get_id(urltext):
    id_regx = re.compile('id=.+')
    ids = id_regx.findall(urltext)
    id = ids[0][3:]
    return id
def preprocess():
    f = open('f407055_4.csv')
    no = 0
    ename = dict([])
    img_name = ''
    iname = ''
    
    for line in f:
        no += 1
        if no == 1:
            continue
        fields = line.split(';')
        if len(fields)<16:
            continue
        #print fields[0]
        ant = fields[15]
        if len(ant) == 0 or ant == '[]':
            continue
        ant = string.replace(ant, '""', '"')[1:-1]
        ant = ant.decode("utf-8")
        try:
            ant = json.loads(ant)
        except:
            continue
        img_name_tmp = ant[0]['src']
        iname = get_id(img_name_tmp) 
        ename[iname] = 1
    print len(ename)
    no = 0
    f2 = open('f407055_4_pro.csv', 'w')
    for intmp in ename:
        f.close()
        f = open('f407055_4.csv')
        k = 0
        for line in f:
            no += 1
            if no == 1:
                continue
            if no == 2:
                temp_line = line
            fields = line.split(';')
            if len(fields)<16:
                continue
            #print fields[0]
            ant = fields[15]
            if len(ant) == 0 or ant == '[]':
                continue
            ant = string.replace(ant, '""', '"')[1:-1]
            ant = ant.decode("utf-8")
            try:
                ant = json.loads(ant)
            except:
                continue
            img_name_tmp = ant[0]['src']
            if intmp == get_id(img_name_tmp) :
                f2.write(line)
                k += 1
        if k==0:
            print intmp+': error'
    f2.write(temp_line)
    f2.close()

if __name__ == '__main__':
    preprocess()