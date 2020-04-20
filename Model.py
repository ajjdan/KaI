"""A simplified U-Net model.
//arxiv.org/pdf/1505.04597
source: https://github.com/mrubash1/keras-semantic-segmentation/blob/develop/src/semseg/models/unet.py
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import tensorflow as tf

from tensorflow.keras.models import Model
from tensorflow.keras.layers import (
    Input, concatenate, Conv2D, MaxPooling2D, UpSampling2D, Activation,
    Reshape, BatchNormalization, Flatten, Dense, Dropout, Conv2DTranspose)
import os

def conv_block(tensor, nfilters, size=3, padding='same', initializer="he_normal"):
    x = Conv2D(filters=nfilters, kernel_size=(size, size), padding=padding, kernel_initializer=initializer)(tensor)
    x = BatchNormalization()(x)
    x = Activation("relu")(x)
    x = Conv2D(filters=nfilters, kernel_size=(size, size), padding=padding, kernel_initializer=initializer)(x)
    x = BatchNormalization()(x)
    x = Activation("relu")(x)
    return x


def deconv_block(tensor, residual, nfilters, size=3, padding='same', strides=(2, 2)):
    y = Conv2DTranspose(nfilters, kernel_size=(size, size), strides=strides, padding=padding)(tensor)
    y = concatenate([y, residual], axis=3)
    y = conv_block(y, nfilters)
    return y


def make_KaI(img_height, img_width, nclasses=2, filters=64):
# down
    input_layer = Input(shape=(img_height, img_width, 3), name='image_input')
    conv1 = conv_block(input_layer, nfilters=filters)
    conv1_out = MaxPooling2D(pool_size=(2, 2))(conv1)
    conv2 = conv_block(conv1_out, nfilters=filters*2)
    conv2_out = MaxPooling2D(pool_size=(2, 2))(conv2)
    conv3 = conv_block(conv2_out, nfilters=filters*4)
    conv3_out = MaxPooling2D(pool_size=(2, 2))(conv3)
    #conv4 = conv_block(conv3_out, nfilters=filters*8)
    #conv4_out = MaxPooling2D(pool_size=(2, 2))(conv4)
    #conv4_out = Dropout(0.5)(conv4_out)
    #conv5 = conv_block(conv4_out, nfilters=filters*16)
    #conv5 = Dropout(0.5)(conv5)
# up
    #deconv6 = deconv_block(conv5, residual=conv4, nfilters=filters*8)
    #deconv6 = Dropout(0.5)(deconv6)
    #deconv7 = deconv_block(deconv6, residual=conv3, nfilters=filters*4)
    #deconv7 = Dropout(0.5)(deconv7) 
    deconv8 = deconv_block(conv3, residual=conv2, nfilters=filters*2)
    deconv9 = deconv_block(deconv8, residual=conv1, nfilters=filters)
# output
    output_layer = Conv2D(filters=2, kernel_size=(1, 1))(deconv9)
    #output_layer = Reshape((128, 128), input_shape=(128,128,1))(output_layer)
    output_layer = BatchNormalization()(output_layer)
    output_layer = Activation('sigmoid')(output_layer)

    model = Model(inputs=input_layer, outputs=output_layer, name='Unet')
    return model