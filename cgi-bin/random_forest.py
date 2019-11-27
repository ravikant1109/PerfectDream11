#Importing the sklearn libraries and packages
from sklearn.ensemble import RandomForestClassifier

#Function that take training data x_train and y_train
#Returns trained object
def model(x_train,y_train,tree) :
    classifier = RandomForestClassifier(n_estimators=tree,criterion='entropy',random_state=0)
    print("Running RandomForest trees degree 2")
    classifier.fit(x_train,y_train)
    return classifier