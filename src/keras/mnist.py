import numpy as np
#import theano
#import theano.tensor as T

import cPickle
import gzip
import os
import sys

## Load Data ##
def load_data(dataset):
    data_dir, data_file = os.path.split(dataset)
    if data_dir == "" and not os.path.isfile(dataset):
        new_path = os.path.join(
            os.path.split(__file__)[0],
            "../..",
            "data",
            dataset
        )
        if os.path.isfile(new_path) or data_file == 'mnist.pkl.gz':
            dataset = new_path

    if (not os.path.isfile(dataset)) and data_file == 'mnist.pkl.gz':
        import urllib
        origin = (
            'http://www.iro.umontreal.ca/~lisa/deep/data/mnist/mnist.pkl.gz'
        )
        print 'Downloading data from %s' % origin
        urllib.urlretrieve(origin, dataset)

    print '... loading data'

    f = gzip.open(dataset, 'rb')
    train_set, test_set, valid_set = cPickle.load(f)
    f.close()
    '''
    def shared_dataset(data_xy, borrow=True):
        data_x, data_y = data_xy
        shared_x = theano.shared(np.asarray(data_x,
                                               dtype=theano.config.floatX),
                                 borrow=borrow)
        shared_y = theano.shared(np.asarray(data_y,
                                               dtype=theano.config.floatX),
                                 borrow=borrow)
        return shared_x, T.cast(shared_y, 'int32')

    test_set_x, test_set_y = shared_dataset(test_set)
    valid_set_x, valid_set_y = shared_dataset(valid_set)
    train_set_x, train_set_y = shared_dataset(train_set)
    '''
    train_set_x, train_set_y = train_set
    test_set_x, test_set_y = test_set
    #valid_set_x, valid_set_y = valid_set
    #rval = [(train_set_x, train_set_y), (valid_set_x, valid_set_y),
    #       (test_set_x, test_set_y)]
    rval = [(train_set_x, train_set_y), (test_set_x, test_set_y)]
    return rval
