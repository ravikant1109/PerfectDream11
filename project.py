from bs4 import BeautifulSoup
from selenium import webdriver
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
		print(self.tournament, end = ":\n")
		print(self.first, end = " vs ")
		print(self.second)
		print(self.time)
		print(self.url)
		print(self.fimg)
		print(self.simg, end = "\n\n")


class Project:
	def __init__(self, url):
		self.url = url
		self.matches = []
	def make_request(self):
		self.driver = webdriver.Firefox()
		self.driver.get(self.url)
		print("connection successful")
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
