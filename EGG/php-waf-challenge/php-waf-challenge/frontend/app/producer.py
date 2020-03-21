# -*- coding: utf-8 -*-
from core.messq import *
from flask import Flask, request, render_template, url_for,redirect,make_response,session,Response
from flask import send_from_directory,send_file
import os,string
from forms.upload_file_form import UploadFileForm
from werkzeug.datastructures import CombinedMultiDict
import random
import hashlib
import requests

Rabbithost = '10.0.20.11'
Rabbituser = 'n1ctf'
Rabbitpass = 'b5d608c6d61'

def random_str():
	return "".join(random.sample(string.ascii_letters+string.digits+"~!@#$%^&*()_+';:?><",16))
def md5(dest):
	m = hashlib.md5()
	m.update(dest.encode())
	return m.hexdigest()
app = Flask(__name__)
app.config['SECRET_KEY']=os.urandom(24)
@app.route('/')
def index():
	rand_s = random_str()
	proof = md5(rand_s)[:6]
	session['proof'] = proof
	return render_template('index.html',content = proof)

@app.route('/check', methods=['POST'])
def checker():
	form = UploadFileForm(CombinedMultiDict([request.form, request.files]))
	if form.validate():
		team = request.form.get('team')
		captcha = request.form.get('captcha')
		if team == "" or captcha == "" :
			return 'Team or Captcha can\'t be NULL.'
		if 'proof' not in session:
			return 'Something error, plz try again.'
		try:
			teamname = requests.get('https://nu1lctf.com/finduserbytoken?token='+team+'&&verified=705e548edbb1b7041cb4dd41f942eb02').text
			print(teamname)
			if teamname!="" and teamname[0]=='{':
				j = json.loads(teamname)
				team = j['team']
			else:
				return 'Your team token error!'
		except:
			return 'Something error, plz try again.'

		if md5(captcha)[:6] == session['proof']:
			waffile = request.files.get('waffile')
			file_content = str(waffile.stream.read(),encoding="unicode_escape")
			expexecQ = MessageQ(Rabbithost,Rabbituser,Rabbitpass,'playerwaf')
			try:
				expexecQ.send(json.dumps({"waf":file_content,"user":team}))	
			except:
				return "Something error, plz try again."
			return "Submit ok.<br>Please visit <a href=\"http://127.0.0.1/\">here</a> to get your score.<br>If you don't have your score updated for a long time, your waf file might be wrong, please check it or submit it once again.<br>"
		else:
			session.clear()
			return 'Captcha error!'
	else:
		print(form.errors)
		return 'File error or Team error!'

if __name__ == '__main__':
	app.run(host='0.0.0.0')