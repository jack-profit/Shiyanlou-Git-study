# _*_ coding:utf-8 _*_
from flask import Flask, render_template, abort
import os
import json

app = Flask(__name__)
file_path = '/home/shiyanlou/files/'

# 读取文件并返回文件内容
def read_file(f_name):
    # 拼接文件路径
    p = os.path.join(file_path, f_name)
    with open(p) as file:
        # 返回文件内容
        return json.load(file)

# 读取目录返回文件名列表
def list_all_file(path):
    files = []
    # 是否为文件目录
    if os.path.isdir(path):
        files = os.listdir(path)
        for x,v in enumerate(files):
            files[x] = v[:-5] # 截取文件名（去掉扩展名 .json）
    return files

@app.route('/')
def index():
    all_files = list_all_file(file_path)
    print(all_files)
    return render_template('index.html', data=all_files)

@app.route('/files/<filename>')
def file(filename):
    # 添加扩展名
    filename += '.json'
    f = os.path.join(file_path, filename)
    # 检查文件是否存在
    if os.path.exists(f):
        # 读取文件内容
        with open(f) as file:
            content = json.load(file)
        return render_template('file.html', data=content)
    else:
        abort(404)
        return render_template('404.html')

@app.errorhandler(404)
def not_find(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    # 测试代码
    files = list_all_file(file_path)
