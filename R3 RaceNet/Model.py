import tflearn
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression

def model(width, height, lr):
    network = input_data(shape=[None, width, height, 3], name='input_pic')

    network = conv_2d(network, 24, 5, activation='elu',strides = 2)
    network = conv_2d(network, 36, 5, activation='elu',strides = 2)
    network = conv_2d(network, 48, 5, activation='elu',strides = 2)
    network = conv_2d(network, 64, 3, activation='elu')
    network = conv_2d(network, 64, 3, activation='elu')

    network = dropout(network, 0.5)
    network = fully_connected(network, 100, activation='elu')
    network = fully_connected(network, 50, activation='elu')
    network = fully_connected(network, 10, activation='elu')
    network = fully_connected(network, 3, activation='softmax')

    network = regression(network, optimizer='adam',
                         loss='categorical_crossentropy',
                         learning_rate=lr, name='targets')

    model = tflearn.DNN(network, checkpoint_path='model_alexnet',
                        max_checkpoints=1, tensorboard_verbose=0, tensorboard_dir='log')

    return model

