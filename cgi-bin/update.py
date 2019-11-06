#!/usr/bin/python3
class Update:
	def __init__(self,data):
		self.data = data
	def run_update(self):
		f = open('../update/header.txt','r')
		header = f.read()
		f.close()
		f = open('../update/footer.txt','r')
		footer = f.read()
		f.close()
		f = open('../update/update.txt','w')
		f.write(self.data)
		f.close()
		self.data = header + self.data +footer
		f = open('../index.html','w')
		f.write(self.data)
		f.close()
