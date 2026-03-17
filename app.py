from flask import Flask, render_template, abort, redirect, url_for, request
from objects import *

app = CustomFlask(__name__)

@app.route('/')
def index():
    module = app.module_num
    return render_template('index1.html', module = module)

@app.route('/', methods=['POST'])
def next_button():
    if 'submit_button' in request.form:
        return redirect(url_for('module'))
    return "An issue occurred."

@app.route('/module')
def module():
    return render_template('index2.html')