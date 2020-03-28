import aiml
import requests
import json
import sqlite3 as sq
import webbrowser
from flask import Flask, render_template, request, jsonify

def db_init():
    conn = sq.connect("conv.db")
    sql='create table if not exists '+'conversation'+'(id INT,user TEXT,bot TEXT)'
    conn.execute(sql)
    conn.commit()
    return conn

def get_id(conn):
    cursor=conn.execute('SELECT id from conversation')
    id=0
    for items in cursor:
	    id=items[0]
    id=id+1
    return id

def insert(u,b,conn,id):
	conn.execute("INSERT INTO conversation (id,user,bot) VALUES (?,?,?) ",(id,u,b))
	conn.commit()

def getelec(conn):
    cur=conn.cursor()
    cur.execute("SELECT elect from electives")
    rows = cur.fetchall()
    res = ', '.join([idx for tup in rows for idx in tup]) 
    print(res)
    return res

def getprof(conn, proflist):
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

def suggest(conn, electlist):
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
    print('worked')

    rows=cur.fetchall()
    res = ', '.join([idx for tup in rows for idx in tup])
    return res

kernel=aiml.Kernel()
kernel.learn("bot/start.aiml")
kernel.respond("learn ai")

app = Flask(__name__)
@app.route("/ask", methods=['POST','GET'])
def ask():
    conn=db_init()
    id=get_id(conn)
    message = str(request.args['chatmessage'])
    resp=kernel.respond(message)
    print(message)
    if str(message)[:6]=="google" or str(message)[:6]=="Google":
	    url = "https://www.google.com.tr/search?q={}".format(str(message)[6:])
	    webbrowser.open(url,2)
	    insert(str(message),"",conn,id)
    
    electives=""
    v=""
    test = resp.split()
    print(test[0])
    if(len(test)==0):
            test.append('empty')

    if(test[0]=='obtain'):
        electives=getelec(conn)
        test.remove('obtain')
        resp=""
        resp="All electives are : "

    elif(test[0]=='fac'):
        check=message.split()
        electives=getprof(conn,check)
        test.remove('fac')
        resp=""
        resp="The electives offered by {} are : ".format(" ".join(test))
    
    elif(test[0] == 'suggest'):
        electlist=test[1:]
        electives=suggest(conn,electlist)
        test.remove('suggest')
        resp=""
        resp="The electives related to {} are : ".format(" ".join(test))

    resp+=electives
    resp=resp.split('newline')
    ch=False
    for item in resp:
        v=v+str(item)
        if 'Bye' in item:
	        return jsonify({"status":"ok", "answer":"exiting"})
    insert(str(message),v,conn,id)
    return jsonify({"status":"ok", "answer":str(v)})
    if ch :
        pass

if __name__ == "__main__":
    app.run(debug=True)