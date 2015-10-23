# On Preprocessing 


1. Preprocessing of the original MNIST data is mainly motivated by practical experience. MNIST digits are normalized such that the width or height of the bounding box equals 20 pixels. The variation of the aspect ratio for various digits is quite large, and we normalize the width of the bounding
box to range from 8 to 20 pixels with a step-size of 2 pixels prior to training for all digits except ones. This results in 7 different training sets. Additionally, we generate a deslanted training set using a PCA algorithm that vertically aligns the principal axis of the digits. The experiments performed with these nine different data sets will henceforth be referred to as the experiments with preprocessed data. Figure 1 shows
ten digits from MNIST preprocessed as described above (left) and the same digits with deformations (right). The first row are original digits. From the second row downwards increasing bounding box normalization from 8 to 20 pixels is applied. The last row shows the deslanted digits.

![Sample Preprocessed Digits](/img/eg01.png)
![Sample Preprocessed Digits](/img/eg02.jpg)

2. Preprocessing steps mentioned in works of [LeCun](http://yann.lecun.com/exdb/mnist/) : **deskewing, noise removal, blurring, width normalization**

3. [Handwritten Digits Recognition using OpenCV](http://perso.ens-lyon.fr/vincent.neiger/publications/report_digit_recognition.pdf)

4. In the second version of the database, the character images are deskewed and cropped down to 20x20 pixel images. The deskewing computes the second moments of inertia of the pixels (counting foreground pixels as one and background pixels as zero) and shears the image by horizontally shifting the lines, so that the principle axis is vertical. 

## References

1. [Better digit recognition with a committee of simple Neural Nets](http://ieeexplore.ieee.org/xpl/login.jsp?tp=&arnumber=6065510&url=http%3A%2F%2Fieeexplore.ieee.org%2Fxpls%2Fabs_all.jsp%3Farnumber%3D6065510)
2. [The MNIST Database of Handwritten Digits](http://yann.lecun.com/exdb/mnist/)
3. [Handwritten Digits Recognition using OpenCV](http://perso.ens-lyon.fr/vincent.neiger/publications/report_digit_recognition.pdf)
4. [Gradient-Based Learning Applied to Document Recognition](http://yann.lecun.com/exdb/publis/pdf/lecun-98.pdf)
