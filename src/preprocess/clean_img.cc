#include "stdio.h"
#include "opencv2/opencv.hpp"
#include "string.h"

using namespace cv;

void morph(Mat* img){
	GaussianBlur(*img, *img, Size(5,5), 0,0, BORDER_DEFAULT);
	adaptiveThreshold(*img,*img,255,1,1,11,2 );
}

void deskew(Mat* img){
	/*
		---- py -----
	m = cv2.moments(img)
	if abs(m['mu02']) < 1e-2:
		return img.copy()
	skew = m['mu11']/m['mu02']
	#print "Skew : %f" %(skew)
	M = np.float32([[1, skew, -0.5*SZ*skew], [0, 1, 0]])
	img = cv2.warpAffine(img,M,(SZ, SZ),flags=affine_flags)
	return img
		---- py -----
	*/
  
  /*
  Mat canny_output;
  vector<vector<Point> > contours;
  vector<Vec4i> hierarchy;

  /// Detect edges using canny
  Canny( src_gray, canny_output, thresh, thresh*2, 3 );
  /// Find contours
  findContours( canny_output, contours, hierarchy, CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE, Point(0, 0) );

  /// Get the moments
  vector<Moments> mu(contours.size() );
  for( int i = 0; i < contours.size(); i++ )
     { mu[i] = moments( contours[i], false ); }
  */
}

int main(int argc, char** argv){

	char file_name[20]; 
	char export_path[20]; 

	//strcpy(file_name,argv[2]);
	//strcpy(export_path,argv[3]);

	Mat src = imread(argv[1], CV_LOAD_IMAGE_GRAYSCALE);

	/*
	 * -- Python Operations --
		src = cv2.resize(src,(120,120), interpolation = cv2.INTER_CUBIC)
		thresh = morph(src).copy()
		deskewed = deskew(thresh)
		deskewed_copy = deskewed.copy()
		roi = roi_op(deskewed_copy,deskewed).copy()
		centered = center(roi)
		centered = dialte(centered)

		# write to file
		writeToFile(thresh,centered,deskewed)
		-------------------------
	*/

	// resize to 120x120
	imshow("source",src);
	resize( src, src, Size(120,120), 0, 0, INTER_LINEAR );
	morph(&src);


	waitKey(0);

	return 0;
}
