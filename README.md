# Deep Tamil
Research on Deep Models for recognizing tamil characters and translation. Currently starting out as a simple OCR project that recognizes tamil characters using a deep Convolutional Neural Network model similar to LeNet5. 


## Modules
1. Preprocessing
2. Training 
3. Testing
4. Prediction
5. Model Integration

## Dataset
The tamil alphabets dataset was downloaded from [Isolated Handwritten Tamil Alphabet Dataset](https://lipitk.sourceforge.net/datasets/tamilchardata.htm). The dataset contained 77.7k samples collected from 170 users, for 155 alphabets(approx. 500 samples for each alphabet). The whole dataset was divided into three sets, training, validation, test datasets. The sample images were preprocessed and the preprocessed images were of size 30x30.

### Preprocessing

*Selective Centering Mechanism*
The samples were centered(based on contour detection) and padded with 10 pixels on all the sides. The samples, were resized to 30x30 and conveted to .png files. Some of the samples were extremely damaged, using them for traning will actually worsen the learned model. Those samples had to be discarded, based on the structural similarity with a standard tamil font set. 

### Traning

We trained totally four model of neural networks, for recognizing the tamil charaset. The model are their accuracy of prediction after traning are as follows.


Model                      | Accuracy(%) 
---------------------------|------------
SingleNeuron               |         30%
SingleLayer                |         33%
MultiLayerPerceptron       |         37%
ConvolutionalNeuralNetwork |         70%


#### CNN in detail:
CNN :- The were two sets of, Conv + ReLu + MaxPooling neural layers. 
It was follwed by a hidden layer of 500 neurons - with activation function **tanh**, and
Output layer of 155 neurons(corresponding each tamil alphabet) - with activation function **softmax**.

The CNN was trained in batches of 128 samples from traning dataset. After each batch the model was validated over validation dataset. 
Then another batch of 128 samples were used to train the CNN. This process was repeated for whole dataset. 

The entire process:- traning over whole training dataset, was repeated for 12 times(12 epochs). Then the model was evaluated with the test dataset. The learned model provided accuracy of 70%.

  


### Plans
Since the tamil alphabet is very different from latin alphabets or numerical digits, the shape of the sample need to changed to a rectangle of 4:3 ratio, say 64x48. 
Also, more samples need to be collected, since the existing dataset is partly damaged and insuffcient for training the neural network, because of the complex nature of tamil alphabets. 
Adding more colvolutional layers will provide more space to store more hypotheses. Storing more hypotheses mean, the model can store more variations in the input. But adding more layers, also dictates the need of more samples, a lot more.
