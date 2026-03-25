from flask import Flask
import os
import json

class CustomFlask(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.module_dict = {}
    
    
    
class Module:
    def __init__(self, title, label, sections: list = [], id = None, href: str = None, objective: str = None):
        self.title = title
        self.label = label
        self.sections = sections
        self.href = href
        self.id = id
        self.objective = objective
        self.json = []
        
        if self.href == None:
            new_label = label.replace(".", "-")
            self.href = f"module{new_label}"
    
    def add_submodule(self, submodule):
        self.sections.append(submodule.format_dict())
    
    def format_dict(self):
        self.id = len(self.json)
        self.dict = {
            "id":self.id,
            "label":self.label,
            "name":self.title,
         }
        
        if len(self.sections) != 0:
            self.dict.update({"sections":self.sections})
        
        else:
            try:
                self.dict.update({"content":self.content})
            except:
                raise ValueError("Object Unknown")
        return self.dict
    
    
class Submodule(Module):
    def __init__(self, parent: Module, content = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.content = content
        
        parent.add_submodule(self)
    

with open('static/json/module_outline.json') as f:
    MODULES = json.load(f)

mod1 = Module(title = "What is a data center?", label = "1.1")

mod2 = Submodule(title = "test", label = "1.1.1", parent = mod1)

print(mod1.format_dict())
