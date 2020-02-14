from __future__ import absolute_import, division, print_function, unicode_literals
import tensorflow as tf

from sklearn.utils.class_weight import compute_class_weight
import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

def get_data_from_npz(path, filename, categorical, class_weighted):
    
    data_dir = tf.keras.utils.get_file(origin="file:" + path, fname=filename)

    with np.load(data_dir) as data:
        train_examples = np.insert(data['x_train'] , [0, 1], 0, axis=1)
        train_labels = np.insert( data['y_train'], [0, 1], 0, axis=1)
        test_labels =  np.insert( data['y_test'] , [0, 1], 0, axis=1)
        test_examples =np.insert(data['x_test'] , [0, 1], 0, axis=1)

       
    num_test_img = test_labels.shape[0]
    num_train_img = train_labels.shape[0]
    img_heigth = 128
    img_width = 200
    num_categories = 2
    
    if categorical is True :
        train_labels_small= train_labels[:,:,:,0].astype(int)
        test_labels_small = test_labels[:,:,:,0].astype(int)
        train_labels_category = keras.utils.to_categorical(train_labels_small).reshape(num_train_img,img_heigth*img_width,num_categories)
        test_labels_category = keras.utils.to_categorical(test_labels_small).reshape(num_test_img,img_heigth*img_width,num_categories)

        return train_examples, test_examples, train_labels_category, test_labels_category
    
    else:

        return train_labels, test_labels
    
    if class_weighted is True:

        df = pd.DataFrame(np.column_stack(train_labels_category))
        # Create a pd.series that represents the categorical class of each one-hot encoded row
        y_classes = df.idxmax(1, skipna=False)

        # Instantiate the label encoder
        le = LabelEncoder()

        # Fit the label encoder to our label series
        le.fit(list(y_classes))

        # Create integer based labels Series
        y_integers = le.transform(list(y_classes))

        # Create dict of labels : integer representation
        labels_and_integers = dict(zip(y_classes, y_integers))

        class_weights = compute_class_weight('balanced', np.unique(y_integers), y_integers)

        return class_weights
    
    datagen = keras.preprocessing.image.ImageDataGenerator()
    #samplewise_center=True,
    #samplewise_std_normalization=True,
    #rotation_range=20,
    #width_shift_range=0.2,
    #height_shift_range=0.2,
    #horizontal_flip=True)

    return datagen

    