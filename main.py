from flask import Flask, request
from flask_cors import *
from extions import db
from model import dbModel
from Crypto.Cipher import AES
import binascii
import base64
import json
import requests
import config
import time

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
CORS(app, supports_credentials=True)
@app.route("/req", methods=["GET", "POST"])

def __init__():
	if request.method == "POST":
		if str(request.form.get("comm")) == "index":
			return index("EiHei?")
		elif str(request.form.get("comm")) == "signin":
			content = None
			try:
				content = str(request.form.get("content"))
			except:
				return insert()
			else:
				return insert(content)
		elif str(request.form.get("comm")) == "toDay":
			return count()
		elif str(request.form.get("comm")) == "query":
			try:
				return query(int(request.form.get("content")))
			except:
				default()
		elif (request.form.get("songids")):
			text = {
				"method": "POST",
				"url": "http://music.163.com/api/song/enhance/player/url",
				"params": {
					"ids": [request.form.get("songids")],
					"br": 320000
				}
			}
			texts = {
				"method": "GET",
				"url": "http://music.163.com/api/song/lyric",
				"params": {
					"id": request.form.get("songids"),
					"lv": -1,
					"tv": -1,
					"kv": -1
				}
			}
			return {
				0: encodeData(text),
				1: encodeData(texts)
			}
	else:
		return default()

def index(parameter):
	return parameter

def insert(content):
	db.create_all()
	a = dbModel(status = "已签到", note = content, date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
	db.session.add(a)
	db.session.commit()
	return "Success"

def query(parameter):
	data = dbModel.query.get(parameter)
	return {
		"id": str(data.id),
		"status": str(data.status),
		"note": str(data.note),
		"date": str(data.date),
		"time": str(data.time)
	}

def count():
	return str(dbModel.query.count())

def default():
	return "Error"

def encodeData(data):
	data = json.dumps(data)
	print(data)
	key = binascii.unhexlify("7246674226682325323F5E6544673A51")
	encryptor = AES.new(key, AES.MODE_ECB)
	pad = 16 - len(data) % 16
	fix = chr(pad) * pad
	byte_data = (data + fix).encode("utf-8")
	return requests.post("http://music.163.com/api/linux/forward", headers = {"Referer": "http://music.163.com/"}, data = {"eparams": binascii.hexlify(encryptor.encrypt(byte_data)).upper().decode()}).text

if __name__ == "__main__":
	app.run(host = "192.168.1.5", port = 5000, debug = True)

