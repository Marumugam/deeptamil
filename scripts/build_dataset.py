#!/usr/bin/python

import cv2
import re
import sys
import numpy as np
import pickle
import os

def convert_image_to_1d_array(img):
    """ Takes path to image and convert it to 1d array and return it"""

    x = cv2.imread(img, cv2.CV_LOAD_IMAGE_GRAYSCALE)
    if x is None:
        print "ERROR: loading image ' + img + ' failed."
        return None
        
    x = cv2.threshold(x, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    if x is None:
        print "ERROR: thresholding image ' + img + ' failed."
        return None

    return x.flatten()



def make_dataset_element(img):
    return (convert_image_to_1d_array(img), 
            int(re.search('u\d+_(\d+)t\d', img).group(1)))




if __name__ == "__main__":
    
    filename = sys.argv[1]
    d = sys.argv[1]
    files = [ f for f in os.listdir(d) if os.path.isfile(os.path.join(d,f)) ]

    i = 0
    t = len(files)
    for f in files:            
        data = convert_image_to_1d_array(os.path.join(d,f))
        if data is None:
            continue

        label  = int(re.search('u\d+_(\d+)t\d', f).group(1))
        
        print '... processing image ' + str(i) + '/' + str(t) + ' --- '  + f + ' '+ str (int(float(i)/float(t) * 100)) + '% complete.'

        if i == 0:
            array_of_data = np.vstack((data,))
            array_of_labels = [label]
            
        else:
            array_of_data = np.vstack((array_of_data, data))
            array_of_labels.append(label)
        
        i =  i + 1

    dataset = (array_of_data, np.asarray(array_of_labels))    
    length = len(dataset)
    #train_len = int(length * 0.8)
    #valid_len = int(length * 0.1)
    #test_len = length - train_len - valid_len

    train_len =  10
    valid_len =  2
    test_len = length - train_len - valid_len

    train_set = (dataset[0][0 : train_len], dataset[1][0 : train_len])
    valid_set = (dataset[0][train_len : train_len + valid_len], dataset[1][train_len : train_len + valid_len])
    test_set = (dataset[0][train_len + valid_len:], dataset[1][train_len + valid_len:])
    pickle.dump((train_set, valid_set, test_set), open('Processed30x30TamilDataSet.pkl', 'wb'))
    
