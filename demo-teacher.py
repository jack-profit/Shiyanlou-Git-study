#!/usr/bin/env python3
import os
import json
from flask import Flask, render_template, abort

app = Flask(__name__)

# wenjianlei
class File:

    # mu biao mu lu lu jing
    directory = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'files')) # tong guo dang qian wen jian lu jing, xiang shang yi ceng, zhao dao files mu lu, zui zhong fan hui mu biao mu lu

    def __init__(self):
        self._files = self._read_all_files()

    def _read_all_files(self):
        result = {}
        # du qu mu biao mu lu, huo qu mu lu li de mei ge wen jian
        for filename in os.listdir(self.directory):
            file_path = os.path.join(self.directory, filename) # mei ge wen jian de lu jing
            # da kai wen jian
            with open(file_path) as f:
                result[filename[:-5]] = json.load(f) # bao liu wen jian ming de fei kuo zhan ming bu fen; du qu wen jian zhong de nei rong
        return result

    def get_title_list(self):
        return [item['title'] for item in self._files.values()]

    def get_by_filename(self, name):
        return self._files.get(name)

# shi li hua bei yong
files = File()

@app.route('/')
def index():
    # shou ye, xian shi mu biao mu lu xia de wen jian qing dan(wen jian ming)
    return render_template('index.html', data=files.get_title_list())

@app.route('/files/<filename>')
def file(filename):
    # yao du qu de wen jian
    file_item = files.get_by_filename(filename)
    if not file_item:
        abort(404)
    return render_template('file.html', data=file_item)

@app.errorhandler(404)
def not_find(error):
    return render_template('404.html'), 404
