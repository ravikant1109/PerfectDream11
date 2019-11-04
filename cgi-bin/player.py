#!/usr/bin/python3
import time
from bs4 import BeautifulSoup
from selenium import webdriver
class Player:
	def __init__(self, name, credit):
		self.name = name
		self.credit = credit
	def print_pl(self):
		return self.name , self.credit

	def open_match(p, match):
		p.driver = webdriver.Firefox()
		p.driver.get(match.url)
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
		data = "<table style='float:left'><caption>WICKETKEEPER</caption>"
		data = data + "<th>Player</th><th>Credit</th>"
		for wk in match.wk:
			name , credit = wk.print_pl()
			data = data + "<tr><td>"+name+"</td><td>"+credit+"</td></tr>"
		data = data + "</table>"
		data = data + "<table style='float:left'><caption>BATSMEN</caption>"
		data = data + "<th>Player</th><th>Credit</th>"
		for batsman in match.batsmen:
			name , credit = batsman.print_pl()
			data = data + "<tr><td>"+name+"</td><td>"+credit+"</td></tr>"
		data = data ="</table>"
		data = data + "<table style='float:right'><caption>ALLROUNDER</caption>"
		data = data + "<th>Player</th><th>Credit</th>"
		for ar in match.ar:
			name , credit = ar.print_pl()
			data = data + "<tr><td>"+name+"</td><td>"+credit+"</td></tr>"
		data = data + "</table>"
		data = data + "<table style='float:right'><caption>BOWLER</caption>"
		data = data + "<th>Player</th><th>Credit</th>"
		for bowler in match.bowlers:
			name , credit = bowler.print_pl()
			data = data + "<tr><td>"+name+"</td><td>"+credit+"</td></tr>"
		data = data + "</table>"
		return data
