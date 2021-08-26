import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
import numpy as np
import os

# present working directory
dirname = os.path.dirname(__file__)

# Helper function to read raw MNIST data
# https://stackoverflow.com/questions/48257255/how-to-import-pre-downloaded-mnist-dataset-from-a-specific-directory-or-folder
def loadMNIST( prefix, folder ):
    intType = np.dtype( 'int32' ).newbyteorder( '>' )
    nMetaDataBytes = 4 * intType.itemsize

    data = np.fromfile( folder + "/" + prefix + '-images-idx3-ubyte', dtype = 'ubyte' )
    magicBytes, nImages, width, height = np.frombuffer( data[:nMetaDataBytes].tobytes(), intType )
    data = data[nMetaDataBytes:].astype( dtype = 'float32' ).reshape( [ nImages, width, height ] )

    labels = np.fromfile( folder + "/" + prefix + '-labels-idx1-ubyte',
                          dtype = 'ubyte' )[2 * intType.itemsize:]

    return data, labels


'''
MNITS DATASET class

This Class adds a layer abstraction for interacting with the MNIST Dataset. It combines the training and testing dataset.

'''
class MNIST_Dataset():
    def __init__(self):
        # load training images and labels
        self.train_images, self.train_labels = loadMNIST( "train", os.path.join(dirname, 'dataset'))
        # load testing images and labels
        self.test_images,self.test_labels = loadMNIST( "t10k", os.path.join(dirname, 'dataset'))
        # concatenate both training and testing to get the 70,000 images
        self.complete_images = np.concatenate((self.train_images,self.test_images),axis = 0)
        # concate both training and testing labels to get the 70,000 labels
        self.complete_labels = np.concatenate((self.train_labels,self.test_labels),axis = 0)

    # helper function to access the label and its corresponding image based on the index
    def __getitem__(self, index):
        data = self.complete_images[index]
        target = self.complete_labels[index]
        return data, target
    # helper function that returns the size of the dataset (i.e 70,000)
    def __len__(self):
        return len(self.complete_images)

index_counter = 0


################################################################################
# Choose Random MNIST image to display to the user

# Input: None
# Output: random MNIST image for UI display

################################################################################

def choose_random_MNIST(index_counter):
    # instantiate dataset
    dataset = MNIST_Dataset()   
    # get data from db
    image,image_label = dataset[index_counter]
    #create Matplotlib figure from grid
    plt.figure(figsize=(15,15))
    #remove axis
    plt.axis("off")
    # show image
    plt.imshow(image,cmap = 'Greys')
    #relative file path from the app.py file
    filepath = os.path.join(dirname, 'static/img/random_MNIST.png')
    # relative file path inside the image occlusion package
    local_filepath = 'static/img/random_MNIST.png'
    # svae image as a jpeg file in the desired 
    plt.savefig(filepath,format='png',bbox_inches='tight')
    plt.close() 
    return image_label,local_filepath,index_counter