#!/usr/bin/python3
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from name import AllNames
import numpy as np
import ensem
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
		return self.name , self.credit
	def open_match(p, match):
		"""!This method will open the perticular match in web browser and fetch the players information and credits from the html returned by the webdriver.
		@param p: Object of class Project
		
		@param match: Object of class project
		"""
		p.driver = webdriver.Firefox()
		p.driver.get(match.url)
		time.sleep(1)
		p.driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/div/div[2]/div[2]/div[1]/button").click()
		p.driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/div/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]").click()
		html = p.driver.page_source
		soup = BeautifulSoup(html, 'html.parser')
		players = soup.findAll('div', attrs = {'class':'playerCardInfoCell_ba412 playerCardInfoContainer_d41f9'})
		for player in players:
			match.wk.append(Player(player.find('div', attrs = {'class':'playerName_73cad'}).text, player.findAll('div', attrs = {'class':'playerCardCell_bf9d8 playerPointsCell_aa0e3'})[1].text))
		p.driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/div/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]").click()
		html = p.driver.page_source
		soup = BeautifulSoup(html, 'html.parser')
		players = soup.findAll('div', attrs = {'class':'playerCardInfoCell_ba412 playerCardInfoContainer_d41f9'})
		for player in players:
			match.batsmen.append(Player(player.find('div', attrs = {'class':'playerName_73cad'}).text, player.findAll('div', attrs = {'class':'playerCardCell_bf9d8 playerPointsCell_aa0e3'})[1].text))
		p.driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/div/div[2]/div[2]/div[1]/div[1]/div[1]/div[3]").click()
		html = p.driver.page_source
		soup = BeautifulSoup(html, 'html.parser')
		players = soup.findAll('div', attrs = {'class':'playerCardInfoCell_ba412 playerCardInfoContainer_d41f9'})
		for player in players:
			match.ar.append(Player(player.find('div', attrs = {'class':'playerName_73cad'}).text, player.findAll('div', attrs = {'class':'playerCardCell_bf9d8 playerPointsCell_aa0e3'})[1].text))
		p.driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/div/div[2]/div[2]/div[1]/div[1]/div[1]/div[4]").click()
		html = p.driver.page_source
		soup = BeautifulSoup(html, 'html.parser')
		players = soup.findAll('div', attrs = {'class':'playerCardInfoCell_ba412 playerCardInfoContainer_d41f9'})
		for player in players:
			match.bowlers.append(Player(player.find('div', attrs = {'class':'playerName_73cad'}).text, player.findAll('div', attrs = {'class':'playerCardCell_bf9d8 playerPointsCell_aa0e3'})[1].text))
		p.driver.quit()
		wk_ = []
		bowler_ = []
		ar_ = []
		batsmen_ = []
		data = "<table style='float:left'><caption>WICKETKEEPER</caption>"
		data = data + "<th>Player</th><th>Credit</th>"
		for wk in match.wk:
			name , credit = wk.print_pl()
			wk_.append(name)
			data = data + "<tr><td>"+name+"</td><td>"+credit+"</td></tr>"
		data = data + "</table>"
		data = data + "<table style='float:left'><caption>BATSMEN</caption>"
		data = data + "<th>Player</th><th>Credit</th>"
		for batsman in match.batsmen:
			name , credit = batsman.print_pl()
			batsmen_.append(name)
			data = data + "<tr><td>"+name+"</td><td>"+credit+"</td></tr>"
		data = data + "</table>"
		data = data + "<table style='float:left'><caption>ALLROUNDER</caption>"
		data = data + "<th>Player</th><th>Credit</th>"
		for ar in match.ar:
			name , credit = ar.print_pl()
			ar_.append(name)
			data = data + "<tr><td>"+name+"</td><td>"+credit+"</td></tr>"
		data = data + "</table>"
		data = data + "<table style='float:left'><caption>BOWLER</caption>"
		data = data + "<th>Player</th><th>Credit</th>"
		for bowler in match.bowlers:
			name , credit = bowler.print_pl()
			bowler_.append(name)
			data = data + "<tr><td>"+name+"</td><td>"+credit+"</td></tr>"
		data = data + "</table>"
		f = open("allcsv.txt", "r")
		second = []
		x = 0
		try:
			while True:
				p = next(f)
				second.append(p)
		except:
			x = 0
		data1 = "<table style='float:left'><caption>WICKETKEEPER</caption>"
		data1 = data1 + "<th>Player</th><th>Score1</th><th>Score2</th><th>Score3</th>"
		nm = AllNames(wk_, second)
		nm.get_players()
		name , indx = nm.all_players()
		scores = ensem.pred(name,indx)
		print(name,scores)
		for i in range(len(scores)):
			print(name[i],scores[i])
			data1 = data1 + "<tr><td>"+name[i]+"</td><td>"+scores[i][0]+"</td><td>"+scores[i][1]+"</td><td>"+scores[i][2]+"</td></tr>"
		data1 = data1 + "<table style='float:left'><caption>Batsman</caption>"
		data1 = data1 + "<th>Player</th><th>Score1</th><th>Score2</th><th>Score3</th>"
		nm = AllNames(batsmen_, second)
		nm.get_players()
		name , indx = nm.all_players()
		scores = ensem.pred(name,indx)
		print(name,scores)
		for i in range(len(scores)):
			print(name[i],scores[i])
			data1 = data1 + "<tr><td>"+name[i]+"</td><td>"+scores[i][0]+"</td><td>"+scores[i][1]+"</td><td>"+scores[i][2]+"</td></tr>"
		data1 = data1 + "<table style='float:left'><caption>All Rounder</caption>"
		data1 = data1 + "<th>Player</th><th>Score1</th><th>Score2</th><th>Score3</th>"
		nm = AllNames(ar_, second)
		nm.get_players()
		name , indx = nm.all_players()
		scores = ensem.pred(name,indx)
		print(name,scores)
		for i in range(len(scores)):
			print(name[i],scores[i])
			data1 = data1 + "<tr><td>"+name[i]+"</td><td>"+scores[i][0]+"</td><td>"+scores[i][1]+"</td><td>"+scores[i][2]+"</td></tr>"
		data1 = data1 + "<table style='float:left'><caption>Bowler</caption>"
		data1 = data1 + "<th>Player</th><th>Score1</th><th>Score2</th><th>Score3</th>"
		nm = AllNames(bowler_, second)
		nm.get_players()
		name , indx = nm.all_players()
		scores = ensem.pred(name,indx)
		print(name,scores)
		for i in range(len(scores)):
			print(name[i],scores[i])
			data1 = data1 + "<tr><td>"+name[i]+"</td><td>"+scores[i][0]+"</td><td>"+scores[i][1]+"</td><td>"+scores[i][2]+"</td></tr>"
		data1 = data1 + "</table>"
		return data , data1