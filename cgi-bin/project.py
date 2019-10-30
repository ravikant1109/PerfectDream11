#!/usr/bin/python3
from bs4 import BeautifulSoup
from selenium import webdriver
import cgitb
cgitb.enable()
import time
import getpass
import requests

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
	def print_match(self):
		if self.time!=None:
			print("<a href='"+self.url+"'>")
			print("<div class='w3-quarter' style='text-align:center'>")
			print("<h3><b>"+self.tournament+"</b></h3>")
			print("<h5 style='color:red'>"+self.time+"</h5>")
			print("<div class='w3-quarter' style='float:left;margin-left:10%'>")
			print("<img src='"+self.fimg+"' style='width:100%' alt='img'>")
			print("<h4>"+self.first+"</h4>")
			print("</div>")
			print("<div class='w3-quarter' style='float:right;margin-right:10%'>")
			print("<img src='"+self.simg+"' style='width:100%' alt='img'>")
			print("<h4>"+self.second+"</h4>")
			print("</div>")
			print("</div></a>")

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
for match in p.matches:
	match.print_match()
