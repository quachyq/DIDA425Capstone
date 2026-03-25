import os

path = os.path.abspath(__file__)
dir = os.path.dirname(path)

with open(f"{dir}/static/txt/module_outline.txt", "r") as f:
    line_list = [line.strip() for line in f if line.strip() != '']
    content = "".join(line_list)

module_dict = {}

for i in line_list:
    if i == "---":
        content_collect = False
        try:
            module_dict.update({"content":" ".join(content_list)})
        except: continue
        
        print(module_dict)
    if content_collect:
        content_list.append(i)
        
    elif i.startswith("label:"):
        module_dict.update({"label": i.split(': ', 1)[1]})
    
    elif i.startswith("title:"):
        module_dict.update({"name": i.split(': ', 1)[1]})
        
    elif i.startswith("content:"):
        content_list = []
        content_collect = True
        
    
