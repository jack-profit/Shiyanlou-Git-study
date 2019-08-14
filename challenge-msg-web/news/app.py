from flask import Flask, render_template, abort
import os
import json

app = Flask(__name__)
file_path = '/home/shiyanlou/files/'

# read file and return content
def read_file(f_name):
    # pin jie wen jian lu jing
    p = os.path.join(file_path, f_name)
    with open(p) as file:
        # fan hui wen jian nei rong
        return json.load(file)

# read path
def list_all_file(path):
    files = []
    # shi fou wei wen jian mu lu
    if os.path.isdir(path):
        files = os.listdir(path)
        for x,v in enumerate(files):
            files[x] = v[:-5] # jie qu wen jian ming
    return files

@app.route('/')
def index():
    all_files = list_all_file(file_path)
    print(all_files)
    return render_template('index.html', data=all_files)


@app.route('/files/<filename>')
def file(filename):
    # kuo zhan ming
    filename += '.json'
    # jian cha wen jian shi fou cun zai
    f = os.path.join(file_path, filename)
    print(os.path.exists(f))
    if os.path.exists(f):
        # du qu wen jian nei rong
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

    files = list_all_file(file_path)

