#!/usr/bin/python3
from bs4 import BeautifulSoup
from selenium import webdriver
from pyvirtualdisplay import Display
import cgitb
cgitb.enable()
import time
import getpass
import requests
import player
from player import Player
from update import Update
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
		## Stores the url of the corresponding match on the Dream11 website.
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
		self.data = ""
	def print_match(self):
		"""This method will print the match data of upcoming matches. The printing will be done in html format for ease of rendering on the website."""
		if self.time!=None:
			self.data = self.data + "<div onclick=\"document.getElementById('"+self.url[-5:]+"').style.display='block'\" onMouseOver=\"this.style.boxShadow='10px 10px 5px grey';this.style.textShadow ='2px 2px 1px grey'\" onMouseOut=\"this.style.boxShadow='10px 10px 5px lightgrey';this.style.textShadow ='2px 2px 1px lightgrey'\" style=\"text-align:center;box-shadow: 10px 10px 5px lightgrey;text-shadow: 2px 2px 1px lightgrey\" class='w3-quarter' style='text-align:center'>"
			self.data = self.data + "<h5><b>"+self.tournament+"</b></h5>"
			self.data = self.data + "<h6 style='color:red'>"+self.time+"</h6>"
			self.data = self.data + "<div class='w3-quarter' style='float:left;margin-left:10%'>"
			self.data = self.data + "<img src='"+self.fimg+"' style='width:100%' alt='img'>"
			self.data = self.data + "<h4>"+self.first+"</h4>"
			self.data = self.data + "</div>"
			self.data = self.data + "<div class='w3-quarter' style='float:right;margin-right:10%'>"
			self.data = self.data + "<img src='"+self.simg+"' style='width:100%' alt='img'>"
			self.data = self.data + "<h4>"+self.second+"</h4>"
			self.data = self.data + "</div>"
			self.data = self.data + "</div>"
		return self.data , self.time , self.url[-5:]
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
		display = Display(visible=0, size=(800, 600))
		display.start()
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
print("Upcoming Matches")
p.parse()
data = ""
for match in p.matches:

	print("Match Details")
	temp , time , idd = match.print_match()
	data = data + temp
	if time!=None:
		data = data + "<div id=\""+idd+"\" class=\"modal\">"
		data = data + "<form class=\"modal-content animate\" action=''>"
		data = data + "<div class=\"container\">"
		data = data + "<h1>Players Details</h1><hr>"
		data = data + Player.open_match(p, match)
		data = data + "<br><div class=\"clearfix\"><button type=\"button\" style=\"width:100%\" onclick=\"document.getElementById('"+idd+"').style.display='none';document.getElementById('id01').style.display='block'\" class=\"cancelbtn\">Predict</button></div><br><div class=\"clearfix\"><button type=\"button\" style=\"width:100%\" onclick=\"document.getElementById('"+idd+"').style.display='none'\" class=\"cancelbtn\">Close</button></div></div></form></div>"
#f = open('/home/rajat/PerfectDream11/PerfectDream11/update/update.txt','w')
#f.write(data)
#f.close()
up = Update(data)
up.run_update()
