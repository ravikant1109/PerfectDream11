import os
import csv
import pickle
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
def pred(name , indx):
	score = []
	x_pred = np.zeros(1499)
	for i in indx:
		x_pred[i] = 1
	x_pred[-3] = 1
	x_pred = [x_pred]
	for i in name:
		print(i)
		with open ("train/"+i+"/"+i+".csv",'r') as csv_read:
			reader = csv.reader(csv_read, delimiter=',')
			data = []
			for j in reader:
				data.append(j)
			data = np.array(data)
			k = 0
			while k<5:
				np.random.shuffle(data)
				k+=1
			x = data[:,0:-1]
			y = data[:,-1]
			x_train = np.array(x)
			y_train = np.array(y)
			# Initialising the Random Forest
			import random_forest
			tree = 10
			rf_classifier = random_forest.model(x_train,y_train,tree)
			rf_score = rf_classifier.predict(x_pred)
			rf_score = str(rf_score[0])
			# Initialising the SVM
			import svm
			svm_classifier = svm.model(x_train,y_train)		
			svm_score = svm_classifier.predict(x_pred)
			svm_score = str(svm_score[0])
			# Initialising the ANN
			import ann

			# ANN1
			in_data = 1499
			h_layer = [512,512]
			out_data = 1
			dropout = [0.0,0.0]
			ann_classifier = ann.model(in_data,h_layer,out_data,dropout,np.array(x_train),np.array(y_train))
			ann_score = ann_classifier.predict(np.array(x_pred))
			ann_score = str(ann_score[0][0])
			score.append([rf_score[0],svm_score[0],ann_score[0]])
	return score
		
'''output = open('train/'+i+'/models_classifier.pkl', 'wb')
pickle.dump([rf_classifier,svm_classifier,ann_classifier], output)
output.close()'''
'''
# Storing trained model
output = open('models_classifier.pkl', 'wb')
pickle.dump([cnn_classifier,rf_classifier,svm_classifier,ann1_classifier,ann2_classifier], output)
output.close()

# Storing trained history
output = open('models_history.pkl', 'wb')
pickle.dump([cnn_history,ann1_history,ann2_history], output)
output.close()
'''