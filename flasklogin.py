#!/usr/bin/env python
# -*- coding: utf-8 -*-
# date : 2019-11-12 17:00:07
__author__ = 'luozaibo'


from flask import Flask, request, render_template
from flask_login import LoginManager


app = Flask(__name__)
login_manager = LoginManager()

# 创建了实际的应用对象，你可以这样配置它来实现登录功能
login_manager.init_app(app)

# @login_manager.user_loader
# def load_user(userid):
#     return User.get(userid)

@app.route('/')
def index():
    return render_template('flask_login.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    return username + '\n' + password
'''
Flask-Login 为 Flask 提供了会话管理。它处理日常的登入、登出并长期保留用户会话。
它会：
存储会话中活动用户的 ID，并允许你随意登入登出。
让你限制已登入（或已登出）用户访问视图。
实现棘手的“记住我”功能。
保护用户会话免遭 Cookie 盗用。
随后可能会与 Flask-Principal 或其它认证扩展集成。


'''

