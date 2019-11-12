#!/usr/bin/env python
# -*- coding: utf-8 -*-
# date : 2019-11-12 17:42:56
__author__ = 'luozaibo'


from flask import Flask, request, render_template
from flask_wtf import FlaskForm
from wtforms import TextField, StringField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    name = StringField('username', validators=[DataRequired()])




'''
功能
集成 wtforms。
带有 csrf 令牌的安全表单。
全局的 csrf 保护。
支持验证码（Recaptcha）。
与 Flask-Uploads 一起支持文件上传。
国际化集成。
FlaskForm就是一个具有CSRF保护的session安全表单了。如果不想CSRF保护，可传入
form = FlaskForm(csrf_enabled=False)
'''