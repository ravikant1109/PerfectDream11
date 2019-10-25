from project import Project
from project import Match
import player as pl

url = "https://www.dream11.com/leagues"
p = Project(url)
p.make_request()
p.parse()
for match in p.matches:
	match.print_match()
pl.open_match(p, p.matches[0])
for wk in p.matches[0].wk:
	wk.print_pl()
print("\n\n")
for bat in p.matches[0].batsmen:
	bat.print_pl()
print("\n\n")
for ar in p.matches[0].ar:
	ar.print_pl()
print("\n\n")
for bowler in p.matches[0].bowlers:
	bowler.print_pl()
