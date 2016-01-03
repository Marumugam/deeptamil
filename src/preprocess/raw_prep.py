#!/usr/bin/env python

import os
import cv2
import numpy as np
import sys
import os

SZ = 120
affine_flags = cv2.WARP_INVERSE_MAP|cv2.INTER_LINEAR

file_name = ""


def morph(src):
	img = cv2.GaussianBlur(src,(5,5),0)
	img = cv2.adaptiveThreshold(img,255,1,1,11,2)
	return img

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
	roi_updated = cv2.resize(roi,(48,w), interpolation = cv2.INTER_CUBIC)
	roi_updated = cv2.resize(roi_updated,(48,48))
	return roi_updated

def center(roi_updated):
	bg = np.zeros((48,64), np.uint8)
	x_offset = 10
	y_offset = 0
	bg[y_offset:y_offset+roi_updated.shape[0], x_offset:x_offset+roi_updated.shape[1]] = roi_updated
	return bg

def deskew(img):
	m = cv2.moments(img)
	if abs(m['mu02']) < 1e-2:
		return img.copy()
	skew = m['mu11']/m['mu02']
	#print "Skew : %f" %(skew)
	M = np.float32([[1, skew, -0.5*SZ*skew], [0, 1, 0]])
	img = cv2.warpAffine(img,M,(SZ, SZ),flags=affine_flags)
	return img

def writeToFile(thresh,centered,deskewed):

	#thresh = cv2.resize(thresh,(30,30), interpolation = cv2.INTER_CUBIC)
	#deskewed = cv2.resize(deskewed,(30,30), interpolation = cv2.INTER_CUBIC)
	#cv2.imwrite(output_path + file_name + "_threshold.png",  thresh)
	#cv2.imwrite(output_path + file_name + "_deskewed.png", deskewed)
	cv2.imwrite(output_path + "/" + file_name + ".jpg", centered)


def display(im):
	cv2.imshow('finale',im)
	cv2.waitKey(0)



def dilate(centered):
	kernel = np.ones((5,5),np.uint8)
	dilation = cv2.dilate(centered,kernel,iterations = 1)
	return dilation

def ind_prep(src):
	#src = cv2.resize(src,(120,120), interpolation = cv2.INTER_CUBIC)
	thresh = morph(src).copy()
	dilated = dilate(thresh)
	deskewed = deskew(dilated)
	deskewed_copy = deskewed.copy()
	roi = roi_op(deskewed_copy,deskewed).copy()
	#centered = center(roi)
	return center(roi)
	#centered = cv2.resize(centered,(30,30), interpolation = cv2.INTER_CUBIC)

'''
if __name__ == '__main__':
	file_path = sys.argv[1]
	output_path = sys.argv[2]
	src = cv2.imread(file_path,0)

	print(sys.argv[0] + ": operating over " + file_path)


	src = cv2.resize(src,(120,120), interpolation = cv2.INTER_CUBIC)

	thresh = morph(src).copy()
	dilated = dilate(thresh)
	deskewed = deskew(dilated)
	deskewed_copy = deskewed.copy()
	roi = roi_op(deskewed_copy,deskewed).copy()
	centered = center(roi)
	centered = cv2.resize(centered,(30,30), interpolation = cv2.INTER_CUBIC)

	file_name, file_ext = os.path.splitext(os.path.basename(file_path))

	#cv2.imwrite(output_path + "/" + file_name + "_orig" + ".jpg", src)
	cv2.imwrite(output_path + "/" + file_name + ".png", centered)

	# display
	#display(thresh,centered,deskewed)

	#cv2.destroyAllWindows()
'''
