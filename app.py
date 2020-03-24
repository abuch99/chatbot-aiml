import aiml
import requests
import json
import sqlite3 as sq
import webbrowser
from flask import Flask, render_template, request, jsonify

conn = sq.connect("conv.db")
sql='create table if not exists '+'conversation'+'(id INT,user TEXT,bot TEXT)'
conn.execute(sql)
conn.commit()
cursor=conn.execute('SELECT id from conversation')

id=0
for items in cursor:
	id=items[0]
id=id+1

def insert(u,b):
	conn.execute("INSERT INTO conversation (id,user,bot) VALUES (?,?,?) ",(id,u,b))
	conn.commit()

kernel=aiml.Kernel()
kernel.learn("bot/start.aiml")
kernel.respond("learn ai")

while True:
    u=input(">>>")
    s=kernel.respond(u)
    if str(u)[:6]=="google" or str(u)[:6]=="Google":
	    url = "https://www.google.com.tr/search?q={}".format(str(u)[6:])
	    webbrowser.open(url,2)
	    insert(str(u),"")
	    continue
    else :
        s=s.split('newline')
        ch=False
        v=""
        for item in s:
            print(str(item))
            v=v+str(item)
            if 'Bye' in item:
	            ch=True
        insert(u,v)
        if ch :
            break