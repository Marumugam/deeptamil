#!/usr/bin/env python

import os
import cv2
import numpy as np
import sys

SZ = 120
affine_flags = cv2.WARP_INVERSE_MAP|cv2.INTER_LINEAR

file_name = ""


def morph(img):
	img = cv2.GaussianBlur(src,(5,5),0)
	img = cv2.adaptiveThreshold(img,255,1,1,11,2)
	return img

def roi_op(img,thresh):
	contours,hierarchy = cv2.findContours(img,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
	# if there are more than one significant contours => complex alphabet
	#	just return the whole image to be resized and centered,
	#		instead of getting the ROI
	num_contours = 0
	for cnt in contours:
		if cv2.contourArea(cnt)>25:
			num_contours = num_contours + 1
			[x,y,w,h] = cv2.boundingRect(cnt)
			roi = thresh[y:y+h,x:x+w]
			#print "ROI shape : ",roi.shape
			# resize roi to 100x100
			roi_100x100 = cv2.resize(roi,(80,80), interpolation = cv2.INTER_CUBIC)

	if num_contours == 1:
		return roi_100x100

	return cv2.resize(thresh,(80,80), interpolation = cv2.INTER_CUBIC)

def center(roi_100x100):
	bg = np.zeros((120,120), np.uint8)
	x_offset=y_offset=10
	bg[y_offset:y_offset+roi_100x100.shape[0], x_offset:x_offset+roi_100x100.shape[1]] = roi_100x100
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


def display(thresh,centered,deskewed):
	cv2.imshow('original',thresh)
	cv2.imshow('centered',centered)
	cv2.imshow('deskewed',deskewed)
	cv2.waitKey(0)

def dilate(centered):
	kernel = np.ones((3,3),np.uint8)
	dilation = cv2.dilate(im,kernel,iterations = 1)


if __name__ == '__main__':
	file_path = sys.argv[1]
	output_path = sys.argv[2]
	src = cv2.imread(file_path,0)

        print(sys.argv[0] + ": operating over " + file_path)

	src = cv2.resize(src,(120,120), interpolation = cv2.INTER_CUBIC)

	thresh = morph(src).copy()
	deskewed = deskew(thresh)
	deskewed_copy = deskewed.copy()
	roi = roi_op(deskewed_copy,deskewed).copy()
	centered = center(roi)
<<<<<<< HEAD
	centered = dialte(centered)
=======
	centered = cv2.resize(centered,(30,30), interpolation = cv2.INTER_CUBIC)
>>>>>>> ac80cb829e90b0402e2eec69a4090c2d9fb3e383

	# write to file
        file_name, file_ext = os.path.splitext(os.path.basename(file_path))
       
        #cv2.imwrite(output_path + "/" + file_name + "_orig" + ".jpg", src)
        cv2.imwrite(output_path + "/" + file_name + file_ext, centered)

	# display
	#display(thresh,centered,deskewed)

	#cv2.destroyAllWindows()
