#!/usr/bin/python3
from bs4 import BeautifulSoup
from selenium import webdriver
import cgitb
cgitb.enable()
import time
import getpass
import requests

class Match:
	""" Match class
	This is a match class which will store upcoming match data fetched from the Dream11 website.
	"""
	def __init__(self, url, tournament, first, second, time, fimg, simg):
		"""!Constructor which will create the match object. Data for some attributes like batsmen will be fetched later.
		@param url: url of perticular match.
		@param tournament: list of tournament.
		@param first: Name of first team.
		@param second: Name of second team.
		@param time: Time remaining to select team.
		@param fimg: Flag image of first team.
		@param simg: Flag image of second team.
		
		"""
		## Stores the url of the corresponding match on the Dream11 website.
		self.url = url
		## Stores the name of the tournament in which the match is held.
		self.tournament = tournament
		## Stores the name of the first team of the cricket match.
		self.first = first
		## Stores the name of the second team of the cricket match.
		self.second = second
		## Time left till the match commences.
		self.time = time
		## Url of the logo of the first team.
		self.fimg = fimg
		## Url of the logo of the second team.
		self.simg = simg
		## List of batsmen participating in the match.
		self.batsmen = []
		## List of bowlers participating in the match.
		self.bowlers = []
		## List of wicket keepers in the match.
		self.wk = []
		## List of all rounders in the match.
		self.ar = []

	def print_match(self):
		"""This method will print the match data of upcoming matches. The printing will be done in html format for ease of rendering on the website."""
		if self.time!=None:
			## Print tournament data in html format.
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
	"""Project Class
	This will open the required website in a browser and will parse the webpage to get required data.
	"""
	def __init__(self, url):
		"""! Constructor which will create the Project object. Initialising required variable.
		@param url: url to open in webbrowser.
		"""
		## Stores url that will open in webbrowser.
		self.url = url
		## Stores the details of matches that are live now.
		self.matches = []
	def make_request(self):
		""" Provide connectivity with the browser using webdriver."""
		## This will provide connectivity with the browser.
		self.driver = webdriver.Firefox()
		self.driver.get(self.url)
	def parse(self):
		""" This parses the opened webpage and generates the data in a useable form."""
		## Stored data in html format.
		html = self.driver.page_source
		## Stores parsed html data to fetch required information.
		soup = BeautifulSoup(html, 'html.parser')
		self.driver.quit()
		##Store list of matches as a list of soups.
		matches = soup.find_all("a", class_="js--match-card matchCard_868db")
		##Retrieve required match data from the list of soups obtained.
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
			##After retrieving required match data, add it to a list of Match objects.
			self.matches.append(Match(url, tournament, first, second, time, fimg, simg))
url = "https://www.dream11.com/leagues"
p = Project(url)
p.make_request()
p.parse()
for match in p.matches:
	match.print_match()
