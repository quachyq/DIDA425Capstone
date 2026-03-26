from flask import Flask
import os
import json
import copy
from pathlib import Path

class CustomFlask(Flask):
    """
    Custom Flask object for initializing app specific attributes
    Includes the directory as an attr
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        path = os.path.abspath(__file__)
        self.dir = os.path.dirname(path)
        self.jinja_env.autoescape = False
        
    def initialize_modules(self):
        """
        Module Initialization Method
        
        Hardcoded the master module instances because theres only 4
        Creates a learning outline list formated as such:
        
        [Module1Json, Module2Json, Module3Json, Module4Json]
        
        See ModuleJson for more info on this object
        """
        main_mod_1 = MasterModule(title = "What Is a Data Center?", label = "1", objective = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.")
        main_mod_2 = MasterModule(title = "What Are the Broad Implications?", label = "2", objective = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.")
        main_mod_3 = MasterModule(title = "What Are the Local Effects?", label = "3", objective = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.")
        main_mod_4 = MasterModule(title = "How Are You Affected and What Can You Do?", label = "4", objective = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.")
        
        main_mod_list = [main_mod_1,main_mod_2,main_mod_3,main_mod_4]
        learning_outline_list = []
        
        # Iterates over the amount of files in static/txt. This is where all module txt files go
        for i in range(len(list(os.scandir(f"{self.dir}/static/txt")))):
            learning_outline_list.append(ModuleJson(ModuleTxt(f"module{i+1}.txt", self.dir), main_mod_list[i]))

        # adds the list jinja vars
        self.jinja_env.globals.update(
            learning_outline_list = learning_outline_list
        )
        
        self.learning_outline_list = learning_outline_list
        
class ModuleTxt:
    """
    ModuleTxt Object used to parse out txt files in the static/txt file.
    Follow the exact syntax that is contained in those files.
    """
    
    def __init__(self, file_name, dir):
        self.dir = dir
        self.file_name = file_name
        self.module_list = []
        self.submodule_list = []
        self.parse_txt()
        
    def parse_txt(self):
        # creates list of lines in txt
        with open(f"{self.dir}/static/txt/{self.file_name}", "r",encoding='utf-8') as f:
            line_list = [line.strip() for line in f if line.strip() != '']
            
        # allocating an empty temporary dict
        module_dict = {}
        
        # looping over lines
        for i in line_list:
            if i == "---":
                # checking for content key in dict
                content_collect = False
                try:
                    
                    # checking if its a submodule/module
                    # copy() is used to avoid pointers (shallow copy)
                    if module_dict["label"].count(".") == 2:
                        self.submodule_list.append(module_dict.copy())
                    else:
                        self.module_list.append(module_dict.copy())
                except: continue

                # clearing after new module detected
                module_dict.clear()
                
            elif content_collect:
                content_list.append(i)
                module_dict.update({"content":" ".join(content_list)})
                
            elif i.startswith("label:"):
                module_dict.update({"label": i.split(': ', 1)[1]})
            
            elif i.startswith("title:"):
                module_dict.update({"name": i.split(': ', 1)[1]})
                
            elif i.startswith("content:"):
                content_list = []
                content_collect = True

class Module:
    """
    Module Object
    
    Attrs::
    
    title: Module title
    label: 1.1
    sections: [Submodule1, ...]
    id: index
    href: autofilled
    
    """
    def __init__(self, title, label, sections=None, id = None, href: str = None):
        self.title = title
        self.label = label
        # This specification is REQUIRED!!!! Types used later (idk for what)
        self.sections = sections if sections is not None else []
        self.href = href
        self.id = int(label[-1]) - 1
        self.json = []
        
        if self.href == None:
            new_label = label.replace(".", "-")
            self.href = f"module{new_label}"
    
    def add_submodule(self, submodule):
        self.sections.append(submodule)
    
    def format_dict(self):
        """
        Method to format the object into a nice jsonable dictionary
        
        Creates the dict as an attr and returns it
        """
        #self.id = len(self.json)
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
                raise ValueError("Module contents unknown")
        return self.dict
    
class MasterModule(Module):
    """
    Defines Masters with a learning objective
    
    Ex. Module 1
    """
    def __init__(self, *args, objective = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.objective = objective
        
class Submodule(Module):
    """
    Submodule with empty section
    """
    def __init__(self, content = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.content = content
        self.sections = []
    
class ModuleJson:
    """
    Object that contains iteratable attrs
    Used for organizing main modules into categories
    
    master_list and dict_master_list contain Module classes that can be called in Jinja
    
    The purpose of this class is for Jinja to interact with for using the {{ x | tojson }} call
    This makes these accessible through JS
    """
    def __init__(self, txt: ModuleTxt, master_module: MasterModule):
        self.txt = txt
        self.master_module = master_module
        self.master_list = []
        self.construct_list()
        self.dict_master_list = [mod.format_dict() for mod in self.master_list]
        
        for i in self.dict_master_list:
            i["sections"] = [section.format_dict() for section in i["sections"]]
        
    def construct_list(self):
        """
        Creates the master list attr.
        
        This contains each each module class.
        """
        for mod in self.txt.module_list:
            temp_module = Module(title=mod["name"], label = mod["label"])
            for submod in self.txt.submodule_list:
                if mod["label"][2] == submod["label"][2]: 

                    temp_module.add_submodule(Submodule(
                        title = submod["name"],
                        label = submod["label"],
                        content = submod["content"]
                            ))
                    
            self.master_list.append(copy.deepcopy(temp_module))
    
    def get_labels(self):
        """
        Returns list of labels the list
        """
        label_list = [mod['label'] for mod in self.dict_master_list]
        return label_list
    
    def find_id_from_label(self, lab):
        """
        does what it says
        """
        for mod in self.dict_master_list:
            if mod["label"] == lab:
                return self.dict_master_list.index(mod)
            
