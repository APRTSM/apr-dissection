from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
import uuid
import json


class BugsList(View):
    template_name = "bug-list.html"

    def get(self, request, *args, **kwargs):    
        with open('./dissection/data/static/defects4j-bugs.json') as file:
            defects = json.load(file)

        with open('./dissection/data/static/classification.json') as file:
            classes = json.load(file)
        

        return render(request, self.template_name, {"defects": defects, "classes": classes, "title": "Dissection"})


class BugDetail(View):
    template_name = "bug-detail.html"

    def get(self, request, *args, **kwargs):    
        with open('./dissection/data/static/defects4j-bugs.json') as file:
            defects = json.load(file)

        for defect in defects:
            if defect['name'] == kwargs['bug_name']:
                break

        patches = []

        with open('./dissection/data/static/apr-efficiency-pfl.json') as file:
            dataset_dictionary = json.load(file)
            
            if defect['name'] in dataset_dictionary:
                patches += dataset_dictionary[defect['name']]

        with open('./dissection/data/dynamic/defects4j-patches.json') as file:
            dataset_dictionary = json.load(file)
            
            if defect['name'] in dataset_dictionary:
                patches += dataset_dictionary[defect['name']]

        return render(request, self.template_name, {
            "bug": defect, 
            "patches": patches,
        })
    
    def post(self, request, *args, **kwargs):
        contributor_name = request.POST['contributor']
        diff = request.FILES['diff'].read().decode("utf-8")
        defect_name = kwargs['bug_name']

        with open('./dissection/data/dynamic/defects4j-patches.json', 'r+') as file:
            patches = json.load(file)

            if defect_name not in patches:
                patches[defect_name] = []

            patches[defect_name].append({
                "contributor": contributor_name,
                "diff": diff,
                "id": uuid.uuid4().hex
            })
            file.seek(0)
            file.write(json.dumps(patches))

        return redirect(reverse('dissection:bug-detail', kwargs={
            'bug_name':defect_name, 
        }))


