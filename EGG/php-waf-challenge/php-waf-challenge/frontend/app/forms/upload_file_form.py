#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Flynn on 2018-07-09 22:39


from wtforms import Form, FileField, StringField
from wtforms.validators import InputRequired,Email
from flask_wtf.file import FileRequired, FileAllowed


class UploadFileForm(Form):
	waffile = FileField(validators=[
		FileRequired()
	])
	team = StringField(validators=[
		InputRequired()
	])
	captcha = StringField(validators=[
		InputRequired()
	])
