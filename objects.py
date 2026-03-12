'''
Object File
'''

from flask import Flask

class CustomFlask(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.module_num = 1
    
    
class Module:
    def __init__(self, content: str):
        self.content = content
        