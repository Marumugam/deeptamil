# import the necessary packages
from skimage.measure import structural_similarity as ssim
import cv2
import os
import sys
import numpy as np
from raw_prep import ind_prep


def build_score(label,_list):
    model = get_model(label)
    _score = []
    for im in _list:
        #print 'im shape', im.shape
        model = cv2.resize(model,(im.shape[1],im.shape[0]))
        #print 'model shape', model.shape
        
        _score.append(ssim(im,model))
    return _score

def get_bbox(contours):
    x = []; y = []
    for cnt in contours:
        x1,y1,w,h = cv2.boundingRect(cnt)
        x.append(x1)
        y.append(y1)
        x.append(x1 + w)
        y.append(y1 + h)
    return min(x),min(y),max(x) - min(x),max(y) - min(y)


def roi_op(img,thresh):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    x,y,w,h = get_bbox(contours)
    roi = thresh[y:y+h,x:x+w]
    roi_100x100 = cv2.resize(roi,(100,100), interpolation = cv2.INTER_CUBIC)
    return roi_100x100

    
def center(roi_100x100):
    bg = np.zeros((120,120), np.uint8)
    x_offset=y_offset=10
    bg[y_offset:y_offset+roi_100x100.shape[0], x_offset:x_offset+roi_100x100.shape[1]] = roi_100x100
    return bg
    
def get_model(label):
    #return ~cv2.resize(cv2.cvtColor(cv2.imread('model_' + label + '.jpg'),cv2.COLOR_BGR2GRAY),(30,30))
    i = ~cv2.cvtColor(cv2.imread('./model/'+str(label).zfill(3)+'.png'),cv2.COLOR_BGR2GRAY)
    i_copy = i.copy()
    roi = roi_op(i_copy,i).copy()
    #return cv2.resize(center(roi),(48,64))
    return center(roi)


    
# separate IO operations and processing
###
##______________ IO _____________##
#
### sort(_based_on_$score_)
## [1]
def build_index(fold):
    index = [ ]
    for file in os.listdir(fold):
        if file.endswith(".tiff"):
            index.append(file)
    return index

def f2im(fold,file_name):
    return cv2.cvtColor(cv2.imread(fold+file_name),cv2.COLOR_BGR2GRAY)
    #return cv2.imread(fold+file_name)
            
def list_io(fold='.'):
    # build an index of file names
    print '>> building index\n'
    idx = build_index(fold)
    print '>> Index built; size : ',len(idx)
    # read images
    print '>> Performing Actual IO; reading Images'
    _list = []
    count = 0
    for id in idx:
        _list.append(f2im(fold,id))
        count = count + 1
        if len(idx) > 1000 and count % 1000 == 0:
            print '>> read %d image' %count
    print '>> IO complete; size : ', len(_list)      
    return idx,_list
            
def preprocess(images,op_folder):
    count = 0
    for img in images:
        pimg = ind_prep(img)
        cv2.imwrite(op_folder +'/'+ str(count) + '.png',pimg)
        count = count + 1
    

if __name__ == '__main__':
    ###
    ## this script takes 3 inputs
    # 1. subfolder of raw dataset, say 134/
    # 2. Label 
    # 3. Output directory
    if len(sys.argv) < 3:
        print '>> need more args'
        sys.exit()
    
    # IO Ops
    #idx,_list = list_io('/home/jbroni/projects/a2tamil/data/def/')
    print 'building index on '+ sys.argv[1]
    idx,_list = list_io(sys.argv[1])
   
    print 'building score on '+ sys.argv[2]
    _score = build_score(sys.argv[2],_list)
    
    _sortable = zip(_list,_score)
    _sortable.sort(key=lambda x: x[1],reverse=True)
    
    #after sorting we need 80% of the list
    filtered_images,score = zip(*_sortable[:int(0.8*len(_sortable))])
    
    print ">> ", len(filtered_images)
    
    
    # we should preprocess the new list and save to Output directory
    preprocessed_images = preprocess(filtered_images,sys.argv[3])
    
    
    #_export(_sortable,sys.argv[1])
    
    
    
##_____________________________##