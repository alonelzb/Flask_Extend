#!/usr/bin/env python
# -*- coding: utf-8 -*-
# date : 2019-11-11 21:06:09
__author__ = 'luozaibo'


import os
from flask import Flask, render_template, redirect, request, send_from_directory, url_for, flash, make_response
from pathlib import Path
from werkzeug.utils import secure_filename
from pypinyin import lazy_pinyin



app = Flask(__name__)
app.config['SECRET_KEY'] = 'luozaibo'
# 上传文 件要储存的目录
UPLOAD_FOLDER = Path.cwd()/'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# 允许上传的文件扩展名的集合。
ALLOWED_EXTEN = {'txt', 'jpg', 'png', 'jpeg', 'mp4', 'py', 'gz', 'pdf'}


@app.route('/')
def index():
    return render_template('upload.html')

# 检查文件名是否合法
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTEN

@app.route('/upload/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files.get('file')
        filename = file.filename

        if filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(filename):
            Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)
            # 把文件保存到 文件系统之前总是要使用这个secure_filename函数对文件名进行安检。
            # name = filename.split('.', 1)[0]
            # ext = filename.split('.', 1)[1]
            # newname = ''.join(lazy_pinyin(name)) + '.' + ext
            # upload_path = UPLOAD_FOLDER/secure_filename(newname)
            upload_path = UPLOAD_FOLDER/filename
            file.save(str(upload_path))
            return redirect(url_for('download', filename=filename))
        
    return render_template('upload.html')#, fileurl=str(upload_path), filename=filename)

@app.route('/download/<filename>/')
def download(filename):
    # 当filename里边出现中文的时候，会报错误, 使用make_response
    # return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

    filepath = UPLOAD_FOLDER
    response = make_response(send_from_directory(filepath, filename, as_attachment=True))
    response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
    return response


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')