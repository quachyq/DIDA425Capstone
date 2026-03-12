import os

path = os.path.abspath(__file__)
dir = os.path.dirname(path)

with open(f"{dir}/static/txt/module_outline.txt", "r") as f:
    line_list = [line.strip() for line in f]
    content = "".join(line_list)
    
module_dict = {}
    
def create_json_module(line_list, module_dict):
    nest_count = 1
    i = 0
    for line in line_list:
        og_nest = nest_count
        if line[0] == "-":
            nest_count = len(line)
            if nest_count > og_nest:
                current_nest = line_list[i+1]
            else: continue
        if line[0].isalpha():
            if nest_count == 1:
                module_dict.update({line:{}})
            if nest_count == 2:
                module_dict[current_nest].update({line:{}})
                
            
                
        i+=1
        
    return module_dict
        

        
    


print(create_json_module(line_list[:-1], {}))
