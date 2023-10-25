from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
import uuid
import json


class BugsList(View):
    template_name = "bug-list.html"

    def get(self, request, *args, **kwargs):    
        with open('./dissection/data/static/original/defects4j-bugs.json') as file:
            defects = json.load(file)

        with open('./dissection/data/static/classification.json') as file:
            classes = json.load(file)
        

        return render(request, self.template_name, {"defects": defects, "classes": classes, "title": "Dissection"})


class BugDetail(View):
    template_name = "bug-detail.html"

    def get(self, request, *args, **kwargs):    
        with open('./dissection/data/static/original/defects4j-bugs.json') as file:
            defects = json.load(file)

        for defect in defects:
            if defect['name'] == kwargs['bug_name']:
                break

        patches = []

        with open('./dissection/data/static/original/apr-efficiency-pfl.json') as file:
            dataset_dictionary = json.load(file)
            
            if defect['name'] in dataset_dictionary:
                patches += dataset_dictionary[defect['name']]

        with open('./dissection/data/dynamic/defects4j-patches.json') as file:
            dataset_dictionary = json.load(file)
            
            if defect['name'] in dataset_dictionary:
                patches += dataset_dictionary[defect['name']]

        return render(request, self.template_name, {
            "defect": defect, 
            "patches": patches,
        })
    
    def post(self, request, *args, **kwargs):
        with open('./dissection/data/static/original/defects4j-bugs.json') as file:
            defects = json.load(file)

        for defect in defects:
            if defect['name'] == kwargs['bug_name']:
                break

        # patches = []

        # with open('./dissection/data/static/original/apr-efficiency-pfl.json') as file:
        #     dataset_dictionary = json.load(file)
            
        #     if defect['name'] in dataset_dictionary:
        #         patches += dataset_dictionary[defect['name']]

        # with open('./dissection/data/dynamic/defects4j-patches.json') as file:
        #     dataset_dictionary = json.load(file)
            
        #     if defect['name'] in dataset_dictionary:
        #         patches += dataset_dictionary[defect['name']]

        # add_patch = True

        # for patch in patches:
        #     if 'tag-name-' + patch['id'] in request.POST.keys():
        #         add_patch = False

        #         break

        # if add_patch:
        contributor_name = request.POST['contributor']
        patch_name = request.POST['name']
        correctness = request.POST['correctness']
        diff = request.FILES['diff'].read().decode("utf-8")

        with open('./dissection/data/dynamic/defects4j-patches.json', 'r+') as file:
            patches = json.load(file)

            if defect['name'] not in patches:
                patches[defect['name']] = []

            patches[defect['name']].append({
                "contributor": contributor_name,
                "name": patch_name,
                "correctness": correctness,
                "diff": diff,
                "id": uuid.uuid4().hex
            })
            file.seek(0)
            file.write(json.dumps(patches))

        # else:
        #     if not 'labels' in patch:
        #         patch['labels'] = []

        #     patch['labels'].append(request.POST['tag-name-' + patch['id']])



        return redirect(reverse('dissection:bug-detail', kwargs={
            'bug_name':defect['name'], 
        }))


