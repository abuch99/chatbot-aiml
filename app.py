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

def getelec():
    cur=conn.cursor()
    cur.execute("SELECT elect from electives")
    rows = cur.fetchall()
    res = ', '.join([idx for tup in rows for idx in tup]) 
    return res

def getprof(proflist):
    cur=conn.cursor()
    if(len(proflist)>1):
        t=tuple(proflist)
    else:
        t=str(proflist[0])

    if(len(proflist )==1):
        query="SELECT subject from profs where name LIKE '{}'".format(t)
    else:
        query="SELECT subject from profs where name in {}".format(t)

    cur.execute(query)
    rows = cur.fetchall()
    res = ', '.join([idx for tup in rows for idx in tup])
    return res

def suggest(electlist):
    cur=conn.cursor()
    if(len(electlist)>1):
        t=tuple(electlist)
    else:
        t=str(electlist[0])

    print(t)

    if(len(electlist)==1):
        query="SELECT subject from suggest where name LIKE '{}'".format(t)
    else:
        query="SELECT subject from suggest where name in {}".format(t)

    cur.execute(query)

    rows=cur.fetchall()
    res = ', '.join([idx for tup in rows for idx in tup])
    return res

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
        electives=""
        test = s.split()
        if(len(test)==0):
            test.append('empty')
        if(test[0]=='obtain'):
            electives=getelec()
            test.remove('obtain')
            s=""
            s="All the electives are :  "

        elif(test[0]=='fac'):
            check=u.split()
            electives=getprof(check)
            test.remove('fac')
            s=""
            s="The electives taken be {} are : ".format(" ".join(test))

        elif(test[0] == 'suggest'):
            electlist=test[1:]
            electives=suggest(electlist)
            test.remove('suggest')
            s=""
            s="The electives related to {} are : ".format(" ".join(test))

        s+=electives
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