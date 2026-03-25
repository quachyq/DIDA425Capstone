from flask import Flask
import os
import json
import copy

class CustomFlask(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ModuleTxt:
    """
    ModuleTxt Object used to parse out txt files in the static/txt file.
    Follow the exact syntax that is contained in those files.
    """
    
    def __init__(self, file_name):
        path = os.path.abspath(__file__)
        self.dir = os.path.dirname(path)
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
    def __init__(self, title, label, sections=None, id = None, href: str = None, objective: str = None):
        self.title = title
        self.label = label
        self.sections = sections if sections is not None else []
        self.href = href
        self.id = id
        self.objective = objective
        self.json = []
        
        if self.href == None:
            new_label = label.replace(".", "-")
            self.href = f"module{new_label}"
    
    def add_submodule(self, submodule):
        self.sections.append(submodule)
    
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
                raise ValueError("Module contents unknown")
        return self.dict
    
    
class Submodule(Module):
    def __init__(self, content = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.content = content
        self.sections = []
    
class ModuleJson:
    def __init__(self, txt: ModuleTxt):
        self.txt = txt
        self.master_list = []
        self.construct_list()
        self.dict_master_list = [mod.format_dict() for mod in self.master_list]
        
    def construct_list(self):

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
        label_list = [mod['label'] for mod in self.dict_master_list]
        return label_list
    
    def find_id_from_label(self, lab):
        for mod in self.dict_master_list:
            if mod["label"] == lab:
                return self.dict_master_list.index(mod)