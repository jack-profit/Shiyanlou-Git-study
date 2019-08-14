#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
import os
import json
from flask import Flask, render_template, abort

app = Flask(__name__)

# 文件类
class File:

    # 目标目录路径
    directory = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'files')) # 通过当前文件路径,进入上一层目录,找到files目录,最终返回目标目录路径

    def __init__(self):
        self._files = self._read_all_files()

    def _read_all_files(self):
        result = {}
        # 读取目标目录,获取目录里的每个文件
        for filename in os.listdir(self.directory):
            file_path = os.path.join(self.directory, filename) # 每个文件的路径
            # 打开文件
            with open(file_path) as f:
                result[filename[:-5]] = json.load(f) # 保留文件名的非扩展名部分作为key；读取文件里的内容
        return result

    def get_title_list(self):
        return [item['title'] for item in self._files.values()]

    def get_by_filename(self, name):
        return self._files.get(name)

# 实例化以备用
files = File()

@app.route('/')
def index():
    # 首页-显示目标目录下的文件清单（文件名）
    return render_template('index.html', data=files.get_title_list())

@app.route('/files/<filename>')
def file(filename):
    # 要读取的文件
    file_item = files.get_by_filename(filename)
    if not file_item:
        abort(404)
    return render_template('file.html', data=file_item)

@app.errorhandler(404)
def not_find(error):
    return render_template('404.html'), 404
