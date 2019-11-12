#!/usr/bin/env python
# -*- coding: utf-8 -*-
# date : 2019-11-12 15:22:11
__author__ = 'luozaibo'


from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import json

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # 正常显示中文
# app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))
api = Api(app)


class Demo(Resource):
    def get(self):
        return jsonify(壁纸='get')

    def post(self):
        data = request.args.get('hello')
        return jsonify(壁纸='post', data=data)


api.add_resource(Demo, '/api','/')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

'''
很多时候在一个 API 中，你的资源可以通过多个 URLs 访问。你可以把多个 URLs 传给 Api 对象的 Api.add_resource() 方法。每一个 URL 都能访问
api.add_resource(Demo, '/api','/')
你也可以为你的资源方法指定 endpoint 参数。

'''