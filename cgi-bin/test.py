#!/usr/bin/python3
import cgitb
cgitb.enable()
from project import Project
from project import Match
import player as pl
from player import Player
url = "https://www.dream11.com/leagues"
p = Project(url)
p.make_request()
p.parse()
for match in p.matches:
	match.print_match()
print(p.matches[0])
Player.open_match(p, p.matches[0])
