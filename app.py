from flask import Flask, render_template, abort, redirect, url_for, request
from objects import *

app = CustomFlask(import_name = __name__)

app.initialize_modules()

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
    # Assign the current working module
    working_module = app.learning_outline_list[int(module_label[0])-1]
    
    # Testing to see if the module is in the index
    try:
        next_mod = working_module.master_list[int(module_label[-1])]
    
    # if not -> we are going to the next main modules
    except:
        if int(module_label[0])!=4:
            next_mod = app.learning_outline_list[int(module_label[0])].master_module
            
    # checking if we are in a main module (redundant?)
    if len(module_label) == 1:
        next_mod = working_module.master_list[0]
        
        return render_template("learn-page.html", current_mod = [{}],
                               obj = working_module.master_module.objective,
                               working_module = working_module,
                               next_mod = next_mod)
    
    if module_label.replace("-",".") not in working_module.get_labels():
        abort(404)
        
    module_id = working_module.find_id_from_label(module_label.replace("-","."))
    current_mod = working_module.dict_master_list[int(module_id)]

    return render_template("learn-page.html",
                           current_mod = current_mod,
                           working_module = working_module,
                            next_mod = next_mod)
