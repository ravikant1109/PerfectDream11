#!/usr/bin/python3
print()
import sqlite3
import cgi
form = cgi.FieldStorage()
email =  form.getvalue("email")
pwd =  form.getvalue('pass')
conn = sqlite3.connect('database/pred11.db')
c = conn.cursor()
data = []
data.append(email)
data.append(pwd)
try:
 	c.execute("SELECT * FROM users WHERE email=? and pass=?",data)
except Exception as e: print(e)
if len(c.fetchall()) == 0:
	print("Wrong Credentials!!")
else:
	print("Login successfull")
conn.commit()
conn.close()
