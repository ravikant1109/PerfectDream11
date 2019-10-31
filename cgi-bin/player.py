#!/usr/bin/python3
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from project import Match
from project import Project

class Player:
	""" Player class
	This is a player class which will store details of players playing in the perticular match.
	"""
	def __init__(self, name, credit):
		"""!Constructor which will create the Player object. Initialising some variables.
		@param name: Name of players.
		
		@param credit: Individual player credit.
		"""
		## Stores player name of some match.
		self.name = name
		## Stores credit given to individual player.
		self.credit = credit
	def print_pl(self):
		"""This method will print the player data of perticular matche. The printing will be done in html format for ease of rendering on the website."""
		print(self.name, end="\t")
		print(self.credit)

	def open_match(p, match):
		"""!This method will open the perticular match in web browser and fetch the players information and credits from the html returned by the webdriver.
		@param p: Object of class Project
		
		@param match: Object of class project
		"""
		p.driver = webdriver.Firefox()
		p.driver.get(match.url)
		time.sleep(1)
		p.driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/div/div[2]/div[2]/div[1]/button").click()
		time.sleep(1)
		p.driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/div/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]").click()
		time.sleep(1)
		html = p.driver.page_source
		soup = BeautifulSoup(html, 'html.parser')
		players = soup.findAll('div', attrs = {'class':'playerCardInfoCell_ba412 playerCardInfoContainer_d41f9'})
		for player in players:
			match.wk.append(Player(player.find('div', attrs = {'class':'playerName_73cad'}).text, player.findAll('div', attrs = {'class':'playerCardCell_bf9d8 playerPointsCell_aa0e3'})[1].text))
		p.driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/div/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]").click()
		time.sleep(1)
		html = p.driver.page_source
		soup = BeautifulSoup(html, 'html.parser')
		players = soup.findAll('div', attrs = {'class':'playerCardInfoCell_ba412 playerCardInfoContainer_d41f9'})
		for player in players:
			match.batsmen.append(Player(player.find('div', attrs = {'class':'playerName_73cad'}).text, player.findAll('div', attrs = {'class':'playerCardCell_bf9d8 playerPointsCell_aa0e3'})[1].text))
		p.driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/div/div[2]/div[2]/div[1]/div[1]/div[1]/div[3]").click()
		time.sleep(1)
		html = p.driver.page_source
		soup = BeautifulSoup(html, 'html.parser')
		players = soup.findAll('div', attrs = {'class':'playerCardInfoCell_ba412 playerCardInfoContainer_d41f9'})
		for player in players:
			match.ar.append(Player(player.find('div', attrs = {'class':'playerName_73cad'}).text, player.findAll('div', attrs = {'class':'playerCardCell_bf9d8 playerPointsCell_aa0e3'})[1].text))
		p.driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/div/div[2]/div[2]/div[1]/div[1]/div[1]/div[4]").click()
		time.sleep(1)
		html = p.driver.page_source
		soup = BeautifulSoup(html, 'html.parser')
		players = soup.findAll('div', attrs = {'class':'playerCardInfoCell_ba412 playerCardInfoContainer_d41f9'})
		for player in players:
			match.bowlers.append(Player(player.find('div', attrs = {'class':'playerName_73cad'}).text, player.findAll('div', attrs = {'class':'playerCardCell_bf9d8 playerPointsCell_aa0e3'})[1].text))
		p.driver.quit()

		for wk in match.wk:
			wk.print_pl()
		print("\n\n")
		for batsman in match.batsmen:
			batsman.print_pl()
		print("\n\n")
		for ar in match.ar:
			ar.print_pl()
		print("\n\n")
		for bowler in match.bowlers:
			bowler.print_pl()

