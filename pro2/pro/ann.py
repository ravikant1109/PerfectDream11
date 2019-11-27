#Importing the libraries and packages
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
import pickle

#Returns trained object
def model(in_data,h_layer,out_data,dropout,x_train,y_train) :
    classifier = Sequential()
    for i in range(len(h_layer)):
        classifier.add(Dense(output_dim = h_layer[i], init='uniform',activation="relu", input_dim = in_data))
        classifier.add(Dropout(dropout[i]))
    classifier.add(Dense(output_dim = out_data, init='uniform'))
    classifier.compile(optimizer = 'adam', loss = 'mean_squared_error', metrics = ['accuracy'])
    classifier.fit(x_train,y_train,batch_size=10,shuffle=True,nb_epoch = 100)
    return classifier
