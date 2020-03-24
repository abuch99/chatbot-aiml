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

    if str(message)[:6]=="google" or str(message)[:6]=="Google":
	    url = "https://www.google.com.tr/search?q={}".format(str(message)[6:])
	    webbrowser.open(url,2)
	    insert(str(message),"",conn,id)

    else :
        resp=resp.split('newline')
        ch=False
        v=""
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