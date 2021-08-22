
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.utils import np_utils
from keras.preprocessing.image import  img_to_array

import numpy as np


import os
from PIL import Image


from sklearn.model_selection import train_test_split

m,n = 240,240

path1='test\\'
path2='train\\'

classes=os.listdir(path2)
x=[]
y=[]
count = 0
for fol in classes:
    print (fol)
    imgfiles=os.listdir(path2 + '\\' + fol);
    for img in imgfiles:
        try:
            im=Image.open(path2+'\\'+fol+'\\'+img);
            im=im.convert(mode='RGB')
            imrs=im.resize((m,n))
            imrs=img_to_array(imrs)/255;
            imrs=imrs.transpose(2,0,1);
            imrs=imrs.reshape(3,m,n);
            x.append(imrs)
            y.append(count)
        except:
            pass
    count += 1

x=np.array(x);
y=np.array(y);

batch_size=32
nb_classes=len(classes)
nb_epoch=20
nb_filters=128
nb_pool=2
nb_conv=3

x_train, x_test, y_train, y_test= train_test_split(x,y,test_size=0.2,random_state=4)

uniques, id_train=np.unique(y_train,return_inverse=True)
Y_train=np_utils.to_categorical(id_train,nb_classes)
uniques, id_test=np.unique(y_test,return_inverse=True)
Y_test=np_utils.to_categorical(id_test,nb_classes)


model= Sequential()
model.add(Convolution2D(nb_filters,nb_conv,nb_conv,padding='valid',input_shape=x_train.shape[1:]))
model.add(Activation('relu'))
model.add(Convolution2D(int(nb_filters/2),nb_conv,nb_conv,padding='same'));
model.add(Activation('relu'))
#model.add(MaxPooling2D(pool_size=(nb_pool,nb_pool)));
model.add(Dropout(0.2))
model.add(Convolution2D(int(nb_filters/4),nb_conv,nb_conv,padding='same'));
model.add(Activation('relu'))
model.add(Convolution2D(int(nb_filters/8),nb_conv,nb_conv,padding='same'));
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(nb_pool,nb_pool),data_format="channels_first"));
model.add(Dropout(0.2));
model.add(Flatten());
model.add(Dense(128));
model.add(Dropout(0.2));
model.add(Dense(nb_classes));
model.add(Activation('softmax'));
model.compile(loss='categorical_crossentropy',optimizer='sgd',metrics=['accuracy'])


nb_epoch=60
batch_size=32
model.fit(x_train,Y_train,batch_size=batch_size,epochs=nb_epoch,verbose=1,validation_data=(x_test, Y_test))

model.save("model_latest.h5",overwrite=True)

files=os.listdir(path1);

img=files[0]
print (img)
im = Image.open(path1 + img);
imrs = im.resize((m,n))
imrs=img_to_array(imrs)/255;
imrs=imrs.transpose(2,0,1);
imrs=imrs.reshape(3,m,n);

x=[]
x.append(imrs)
x=np.array(x);
predictions = model.predict(x)
print (predictions)
print (model.summary())