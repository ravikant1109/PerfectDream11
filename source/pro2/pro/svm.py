#Importing the sklearn libraries and packages
from sklearn.svm import SVR

#Function that take training data x_train and y_train
#Returns trained object
def model(x_train,y_train):
    classifier = SVR(kernel='rbf',gamma='auto')
    print("Running SVM 'poly' degree 2")
    classifier.fit(x_train,y_train)
    return classifier