from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
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
            if defect['bugId'] == kwargs['bug_id'] and defect['project'] == kwargs['bug_project']:
                bug = defect

                break

        bug_project_and_id = kwargs['bug_project'] + '_' + str(kwargs['bug_id'])

        patches = []

        with open('./dissection/data/static/apr-efficiency-pfl.json') as file:
            dataset_dictionary = json.load(file)
            
            if bug_project_and_id in dataset_dictionary:
                patches += dataset_dictionary[bug_project_and_id]

        with open('./dissection/data/dynamic/defects4j-patches.json') as file:
            dataset_dictionary = json.load(file)
            
            if bug_project_and_id in dataset_dictionary:
                patches += dataset_dictionary[bug_project_and_id]

        return render(request, self.template_name, {
            "bug": bug, 
            "bug_project_and_id": bug_project_and_id, 
            "patches": patches
        })
    
    def post(self, request, *args, **kwargs):
        contributor_name = request.POST['contributor']
        diff = request.FILES['diff'].read().decode("utf-8")
        bug_project_and_id = kwargs['bug_project'] + '_' + str(kwargs['bug_id'])

        with open('./dissection/data/dynamic/defects4j-patches.json', 'r+') as file:
            patches = json.load(file)

            if bug_project_and_id not in patches:
                patches[bug_project_and_id] = []

            patches[bug_project_and_id].append({
                "contributor": contributor_name,
                "diff": diff
            })
            file.seek(0)
            file.write(json.dumps(patches))

        return redirect(reverse('dissection:bug-detail', kwargs={
            'bug_project':kwargs['bug_project'], 
            'bug_id' : str(kwargs['bug_id'])
        }))


