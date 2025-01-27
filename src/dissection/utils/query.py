from . import config
import json
import pickle


def get_all(file_name):
    if file_name.endswith(".json"):
        with open(config.DATA_DIR + file_name) as file:
            return json.load(file)

    elif file_name.endswith(".pkl"):
        with open(config.DATA_DIR + file_name, "rb") as file:
            return pickle.load(file)
        
    else:
        raise ValueError("Invalid file format")
    
def save(file_name, dataset):
    if file_name.endswith(".json"):
        with open(config.DATA_DIR + file_name, "w") as file:
            file.seek(0)
            file.write(json.dumps(dataset))

    elif file_name.endswith(".pkl"):
        with open(config.DATA_DIR + file_name, "wb") as file:
            pickle.dump(dataset, file)
        
    else:
        raise ValueError("Invalid file format")


def read_file(file_name):
    if file_name.endswith(".patch"):
        with open(config.PATCH_DATA_DIR + file_name) as file:
            return file.read()

def commit(file_name, dataset):
    with open(config.DATA_DIR + file_name, "w") as file:                
        file.seek(0)
        file.write(json.dumps(dataset))

def add_object(file_name, item):
    items = get_all(file_name)
    items.append(item)
    
    commit(file_name, items)

def get_objects_by_feature(dataset, feature, value):
    items = []

    for item in dataset:
        if item[feature] == value:
            items.append(item)

    return items

def get_object_by_unique_feature(dataset, feature, value):
    for item in dataset:
        if item[feature] == value:
            return item

def get_object_by_id(dataset, id):
    for item in dataset:
        if item["id"] == id:
            return item

def get_foreign_key_pairs(dataset, foreign_key_field_name):
    pairs = {}

    for item in dataset:
        try:
            pairs[item[foreign_key_field_name]].append(item)

        except:
            pairs[item[foreign_key_field_name]] = [item]

    return pairs

    
