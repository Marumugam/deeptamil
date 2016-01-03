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
    
    print(sys.argv)
    d = sys.argv[1]
    dest = sys.argv[2]
    _dirs = [ f for f in os.listdir(d) if os.path.isdir(os.path.join(d,f)) ]
    
    print "dirs: " + str(_dirs)
    first = True

    for _dir in _dirs:
        print "under dir: " + _dir
        i = 0
        files = [ f for f in os.listdir(d + _dir) if os.path.isfile(os.path.join(d + _dir,f)) ]
        t = len(files)
        for f in files:            
            print ' ... processing image ' + str(i) + '/' + str(t) + ' --- '  + f + ' '+ str (int(float(i)/float(t) * 100)) + '% complete.'
            data = convert_image_to_1d_array(os.path.join(d + _dir,f))
            if data is None:
                continue

            label = int(_dir)

            if first:
                array_of_data = np.vstack((data,))
                array_of_labels = [label]
                first = False

            else:
                array_of_data = np.vstack((array_of_data, data))
                array_of_labels.append(label)
        
            i =  i + 1
            print(" ... added image " + str(f) + " with label " + str(label)) 

    dataset = (array_of_data, np.asarray(array_of_labels))    
    length = dataset[0].shape[0]
    width = dataset[0].shape[1]

    train_len = int(length * 0.8)
    valid_len = int(length * 0.1)
    test_len = length - train_len - valid_len

    #train_len =  10
    #valid_len =  2
    #test_len = length - train_len - valid_len

    print("shuffling the dataset...")

    shuffled = np.column_stack((array_of_data, np.asarray(array_of_labels)))
    np.random.shuffle(shuffled)
                               
    dataset = (shuffled[:,:width], shuffled[:,-1:])

    train_set = (dataset[0][0 : train_len], dataset[1][0 : train_len])
    valid_set = (dataset[0][train_len : train_len + valid_len], dataset[1][train_len : train_len + valid_len])
    test_set = (dataset[0][train_len + valid_len:], dataset[1][train_len + valid_len:])

    print ("writing pickle to file: " + dest + ".pkl")
    pickle.dump((train_set, valid_set, test_set), open(dest + '.pkl', 'wb'))
    
