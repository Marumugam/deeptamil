# Meta

*design and development tasks are documented here*

## Dataset Generation

*assigned to @vanangamudi*

### Raw dataset Organization

1. Download raw datasets from [here](lipitk.sourceforge.net/datasets/tamilchardata.htm)
2. The dataset is organized into multiple folders. Each folder contains characters written by an individual. Folder name format **usr_xxx**. Inside each folder, there are *.tiff images of characters. Each character is written 10 times (10 images per character) by the same person.

### Preprocessing

1. The python script src/preprocess/_main.py runs a few operations on an image (tiff) and exports a png file to given path

2. Usage : 

``` python
*./main_py /path/to/file_name.tiff file_name_without_extension /path/to/export/output
```

3. Modify the *loop* script in src/preprocess to loop through images running _main.py


### Training, Testing Requirements

*notice that after preprocessing all the raw images, we should create train/ and test/ folders and store the preprocessed images in them*

1. We need two folders of preprocessed images. One folder containing 80% of total images for training and the other containing 20% images for testing. 

2. In the train folder, each image should be named in the format **uxxx_yyytzzz.png**, where *xxx* : userid, *yyy* : character code (000 for the first vowel), *zzz* : nth replica of character *yyy*

3. Same goes for test/ folder

### Indexing

1. We need two index files, one for train/ set and other for test/ set

2. The index file is a simple text files with 2 columns, tab separated

3. Column 1 : file path of image ( /path/to/image_file.png )

4. Column 2 : label of image ( Character code the image represents ) **Note : leading zeros should not be part of the label**

5. Output : traindata.index, testdata.index


