'''
Object File
'''

from flask import Flask

class CustomFlask(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.module_num = 1
    
class Module:
    def __init__(self, content: str, href: str,):
        self.content = content
        self.href = href

class Submodule(Module):
    def __init__(self, subnum, *args):
        super().__init__(*args)
        self.subnum = subnum