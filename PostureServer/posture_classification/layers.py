from keras.layers import Activation
from keras.regularizers import l2
from keras.layers.convolutional import Conv2D
from keras.layers.pooling import MaxPooling2D
from keras.initializers import random_normal, constant


def relu(input_tensor):
        tensor = Activation('relu')(input_tensor)

        return tensor


def convolution(input_tensor, number_of_filters, kernel_size, name, weight_decay):
    kernel_regularization = l2(weight_decay[0]) if weight_decay else None
    bias_regularization = l2(weight_decay[1]) if weight_decay else None

    tensor = Conv2D(number_of_filters, (kernel_size, kernel_size), padding='same', name=name,
                    kernel_regularizer=kernel_regularization,
                    bias_regularizer=bias_regularization,
                    kernel_initializer=random_normal(stddev=0.01),
                    bias_initializer=constant(0.0))(input_tensor)

    return tensor


def pooling(input_tensor, pooling_size, pooling_stride, name):
    tensor = MaxPooling2D((pooling_size, pooling_size), strides=(pooling_stride, pooling_stride), name=name)(input_tensor)

    return tensor