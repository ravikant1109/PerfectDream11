#!/usr/bin/python3
from bs4 import BeautifulSoup
from selenium import webdriver
import cgitb
cgitb.enable()
import time
import getpass
import requests
from update import Update
class Match:
	def __init__(self, url, tournament, first, second, time, fimg, simg):
		self.url = url
		self.tournament = tournament
		self.first = first
		self.second = second
		self.time = time
		self.fimg = fimg
		self.simg = simg
		self.batsmen = []
		self.bowlers = []
		self.wk = []
		self.ar = []
		self.data = ""
	def print_match(self):
		if self.time!=None:
			self.data = self.data + "<a href='"+self.url+"'>"
			self.data = self.data + "<div class='w3-quarter' style='text-align:center'>"
			self.data = self.data + "<h3><b>"+self.tournament+"</b></h3>"
			self.data = self.data + "<h5 style='color:red'>"+self.time+"</h5>"
			self.data = self.data + "<div class='w3-quarter' style='float:left;margin-left:10%'>"
			self.data = self.data + "<img src='"+self.fimg+"' style='width:100%' alt='img'>"
			self.data = self.data + "<h4>"+self.first+"</h4>"
			self.data = self.data + "</div>"
			self.data = self.data + "<div class='w3-quarter' style='float:right;margin-right:10%'>"
			self.data = self.data + "<img src='"+self.simg+"' style='width:100%' alt='img'>"
			self.data = self.data + "<h4>"+self.second+"</h4>"
			self.data = self.data + "</div>"
			self.data = self.data + "</div></a>"
		return self.data
class Project:
	def __init__(self, url):
		self.url = url
		self.matches = []
	def make_request(self):
		self.driver = webdriver.Firefox()
		self.driver.get(self.url)
	def parse(self):
		html = self.driver.page_source
		soup = BeautifulSoup(html, 'html.parser')
		self.driver.quit()
		matches = soup.find_all("a", class_="js--match-card matchCard_868db")
		for match in matches:
			url = match['href']
			if url != "":
				url = "https://www.dream11.com" + url
			tournament = match.find("div", attrs = {'class': 'js-match-card-header matchCardHeaderTitle_c5373 matchCardHeaderTitleDesktop_a2024'}).text
			first = match.find("div", attrs = {'class':'squadShortName_a116b squadShortNameLeft_db179'}).text
			second = match.find("div", attrs = {'class':'squadShortName_a116b squadShortNameRight_42ab0'}).text
			time = match.find("div", attrs = {'class':'matchCardTimer_a5620 matchCardTimerDesktop_48a55'})
			if time != None:
				time = time.text
			imgs = match.findAll("img", attrs = {'class':'lazyLoaderImg_0ab5d lazyLoaderImgFit_49680 lazyLoaderImgLoaded_cf703'})
			fimg = imgs[0]['src']
			simg = imgs[1]['src']
			self.matches.append(Match(url, tournament, first, second, time, fimg, simg))
url = "https://www.dream11.com/leagues"
p = Project(url)
p.make_request()
p.parse()
data = ""
for match in p.matches:
	data = data + match.print_match()
#f = open('/home/rajat/PerfectDream11/PerfectDream11/update/update.txt','w')
#f.write(data)
#f.close()
up = Update(data)
up.run_update()
