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

app = Flask(__name__)
@app.route("/ask", methods=['POST','GET'])
def ask():
    message = str(request.args['chatmessage'])
    resp=kernel.respond(message)

    if str(message)[:6]=="google" or str(message)[:6]=="Google":
	    url = "https://www.google.com.tr/search?q={}".format(str(message)[6:])
	    webbrowser.open(url,2)
	    insert(str(message),"")

    else :
        resp=resp.split('newline')
        ch=False
        v=""
        for item in resp:
            return jsonify({"status":"ok", "answer":str(item)})
            v=v+str(item)
            if 'Bye' in item:
	            ch=True
        insert(message,resp)
        if ch :
            pass

if __name__ == "__main__":
    app.run(debug=True)