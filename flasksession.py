#!/usr/bin/env python
# -*- coding: utf-8 -*-
# date : 2019-11-12 20:21:01
__author__ = 'luozaibo'


from flask import Flask, render_template, request, redirect, session
from flask_session import Session
import redis

# session = Session()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'luozaibo'
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.StrictRedis(host='localhost', port=6379, db=2)
Session(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    session['username'] = 'zbluo'
    name = session.get('username')
    return name