def get_object_by_id(dataset, id):
    for item in dataset:
        if item["id"] == id:
            break

    return item