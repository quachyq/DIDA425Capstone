from flask import Flask, render_template, abort, redirect, url_for, request, render_template_string
import requests
from objects import *

app = CustomFlask(import_name = __name__)

app.initialize_modules()

@app.route('/devtest')
def test():
    return render_template('sandbox.html')

@app.route('/map')
def map():
    return render_template('map_widget.html')

@app.route('/datacenter-interactive')
def interactive_datacenter():
    return render_template('datacenter_3d.html')

@app.route('/')
def index():
    return render_template('title-page.html')

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
    # Assign the current working module
    working_module = app.learning_outline_list[int(module_label[0])-1]
    
    # Testing to see if the module is in the index
    try:
        next_mod = working_module.dict_master_list[int(module_label[-1])]
    
    # if not -> we are going to the next main modules
    except:
        if int(module_label[0])!=4:
            next_mod = app.learning_outline_list[int(module_label[0])].master_module
            
    # checking if we are in a main module (redundant?)
    if len(module_label) == 1:
        next_mod = working_module.dict_master_list[0]
        prev_mod = app.learning_outline_list[int(module_label[0])-2].dict_master_list[-1]
        print(prev_mod["label"])
        return render_template("learn-page.html", current_mod = [{}],
                               obj = working_module.master_module.objective,
                               working_module = working_module,
                               next_mod = next_mod,
                               prev_mod=prev_mod)
    
    if module_label.replace("-",".") not in working_module.get_labels():
        abort(404)
        
    module_id = working_module.find_id_from_label(module_label.replace("-","."))
    current_mod = working_module.dict_master_list[int(module_id)]
    if module_id != 0:
        prev_mod = working_module.dict_master_list[int(module_id) - 1]
    else:
        prev_mod = working_module.master_module.format_dict()
    print(prev_mod["label"])
        
    try:

        return render_template("learn-page.html",
                           current_mod = current_mod,
                           working_module = working_module,
                            next_mod = next_mod,
                            prev_mod = prev_mod)
        
    except UnboundLocalError:
        return render_template("learn-page.html",
                               current_mod = current_mod,
                               working_module = working_module,
                                prev_mod = prev_mod)
        