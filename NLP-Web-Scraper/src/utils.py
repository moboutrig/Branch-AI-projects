import json
    
def save_json(content:list, filename='data.json'):
    json_object = json.dumps(content, indent=4)
    
    with open("results/"+filename, "w") as outfile:
        outfile.write(json_object)
    
def read_json(user_selection:int):
    
    filename = 'CNN.json' if user_selection <= 1 else 'IGN.json'
    
    f = open('results/'+filename)
    file_content = json.load(f)
    f.close()
    return file_content

