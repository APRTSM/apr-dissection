from . import config
import json


def get_all(file_name):
    with open(config.DATA_DIR + file_name) as file:
        return json.load(file)

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

def get_object_by_id(dataset, id):
    for item in dataset:
        if item["id"] == id:
            break

    return item
