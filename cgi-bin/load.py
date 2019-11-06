#!/usr/bin/python3
import cgitb
cgitb.enable()
print()
f = open('update.txt','r')
update = f.read()
print(update)
