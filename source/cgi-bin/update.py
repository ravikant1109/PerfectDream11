#!/usr/bin/python3
import os
class Update:
	def run_update(self):
		f = open("../update/header.txt","r")
		data = f.read()
		f.close()
		for i in os.listdir('../update/match/'):
			f = open('../update/match/'+i+'/update.txt',"r")
			data = data + f.read()
			f.close()
		f = open('../update/footer.txt','r')
		data = data + f.read()
		f.close()
		f = open('../index.html','w')
		f.write(data)
		f.close()