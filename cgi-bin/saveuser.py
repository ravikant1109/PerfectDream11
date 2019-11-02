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
try:
 	c.execute("SELECT * FROM users WHERE email=?",data)
except Exception as e: print(e)

if len(c.fetchall()) == 0:
	data.append(pwd)
	try:
 		c.execute("INSERT INTO users VALUES (?,?)",data)
 		print("SignUp successfull")
	except Exception as e: print(e)
else:
	print("Email already exits")
conn.commit()
conn.close()
