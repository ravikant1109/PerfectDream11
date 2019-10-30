#!/usr/bin/python3
import cgitb
cgitb.enable()
from project import Project
from project import Match
import player as pl
url = "https://www.dream11.com/leagues"
p = Project(url)
p.make_request()
p.parse()
for match in p.matches:
	match.print_match()
#pl.open_match(p, p.matches[0])
