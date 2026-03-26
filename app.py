from flask import Flask, render_template, abort, redirect, url_for, request
from objects import *

app = CustomFlask(import_name = __name__)

modules = ModuleJson(ModuleTxt("module_outline.txt"))
modules_list = modules.master_list

app.jinja_env.globals.update(
    modules = modules,
    modules_list = modules_list
)

@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/', methods=['POST'])
def next_button():
    if 'submit_button' in request.form:
        return redirect(url_for('outline'))
    return "An issue occurred."

@app.route('/learn-page')
def learn_page():
    return render_template('learn-page.html')

@app.route('/module-outline')
def outline():
    return render_template('module-outline.html')

@app.route("/learn-page/module<module_label>")
def module(module_label):
    if module_label.replace("-",".") not in modules.get_labels():
        abort(404)
        
    module_id = modules.find_id_from_label(module_label.replace("-","."))
    current_mod = modules_list[int(module_id)]

    return render_template("learn-page.html", current_mod = current_mod)
