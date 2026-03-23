from flask import Flask
import os
import json

class CustomFlask(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.module_dict = {}
    
    
    
class Module:
    def __init__(self, id, title, href: str = None, content: str= None, objective: str = None):
        self.content = content
        self.title = title
        self.href = href
        self.id = id
        self.objective = objective
        self.nested = {}
        
        if self.href == None:
            self.href = f"module{id.replace(".","-")}"
        
    def add_nest(self, module):
        self.nested.update({module.id: module})

with open('static/json/module_outline.json') as f:
    MODULES = json.load(f)

mod1 = Module(id="1.1", title = "What is a data center?")