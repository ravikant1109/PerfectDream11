#!/usr/bin/python3
class Update:
	def __init__(self,data):
		self.data = data
	def run_update(self):
		f = open('/home/rajat/PerfectDream11/PerfectDream11/update/header.txt','r')
		header = f.read()
		f.close()
		f = open('/home/rajat/PerfectDream11/PerfectDream11/update/footer.txt','r')
		footer = f.read()
		f.close()
		#f = open('/home/rajat/PerfectDream11/PerfectDream11/update/update.txt','r')
		#update = f.read()
		#f.close()
		self.data = header + self.data +footer
		f = open('/home/rajat/PerfectDream11/PerfectDream11/index.html','w')
		f.write(self.data)
		f.close()
