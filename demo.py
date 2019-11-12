#!/usr/bin/env python
# -*- coding: utf-8 -*-
# date : 2019-11-11 21:06:09
__author__ = 'luozaibo'


import os
from flask import Flask, render_template,  request, url_for
from flask_uploads import UploadSet, configure_uploads, DEFAULTS, ARCHIVES, patch_request_class, ALL
from pathlib import Path
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['SECRET_KEY'] = 'luozaibo'
# 创建上传集， ALL允许所有文件，IMAGES图片， TEXT = ('txt',) ,ARCHIVES = ('gz bz2 zip tar tgz txz 7z')
fileset = UploadSet('files', ALL)
# 文件储存地址, 注意 FILES与files对应
UPLOADED_FILES_DEST = Path()/'upload'
# UPLOADED_FILES_DEST = os.getcwd() + '/upload'
app.config['UPLOADED_FILES_DEST'] = UPLOADED_FILES_DEST
# 文件大小限制，def patch_request_class(app, size=64 * 1024 * 1024):
# patch_request_class(app)
# It will also register the uploads module if it hasn't been set.
configure_uploads(app, fileset)


@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files.get('file')
        filename = fileset.save(file)
        fileurl = fileset.url(filename)
        filepath = fileset.path(filename)
        return fileurl

    return render_template('upload.html')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

'''

DEFAULTS = TEXT + DOCUMENTS + IMAGES + DATA
def patch_request_class(app, size=64 * 1024 * 1024):
def configure_uploads(app, upload_sets):
class UploadConfiguration(object):
    def __init__(self, destination, base_url=None, allow=(), deny=()):
class UploadSet(object):
    def __init__(self, name='files', extensions=DEFAULTS, default_dest=None):
        name:名字，必须和配置的名字相对应；
        extensions：设置允许的文件扩展名；
        default_dest ：设置默认的上传文件路径；
    basename = self.get_basename(storage.filename)
    UploadSet.url(filename):返回filename下载的url路径；
UploadSet.path(filename):返回filename的绝对路径，不会检查该文件是否存在；
UploadSet.config:返回配置；
UploadSet.save(self, storage, folder=None, name=None)：参数传入文件流werkzeug.FileStorage对象，folder为子目录，name保存为另一个名字，.结尾的话保留源文件的扩展名；
'''