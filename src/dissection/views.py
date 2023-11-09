import json
from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
from .utils import config, query


class BugsList(View):
    template_name = "bug-list.html"

    def get(self, request, *args, **kwargs):    
        with open(config.DATA_DIR + "bugs.json") as file:
            bugs = json.load(file)
        
        with open(config.DATA_DIR + "benchmarks.json") as file:
            benchmarks = json.load(file)

        return render(request, self.template_name, {"bugs": bugs, "benchmarks": benchmarks, "title": "List of Bugs"})


class BugDetail(View):
    template_name = "bug-detail.html"

    def get(self, request, *args, **kwargs):    
        with open(config.DATA_DIR + "bugs.json") as file:
            bugs = json.load(file)

        with open(config.DATA_DIR + "patches.json") as file:
            patches = json.load(file)

        with open(config.DATA_DIR + "tags.json") as file:
            tags = json.load(file)

        for bug in bugs:
            if bug['name'] == kwargs['bug_name']:
                break

        selected_patches = []

        for patch in patches:
            if patch["bugId"] == bug["id"]:
                selected_patches.append(patch)

        return render(request, self.template_name, {
            "bug": bug, 
            "patches": selected_patches,
            "tags": tags,
        })
    
    def post(self, request, *args, **kwargs):
        with open(config.DATA_DIR + "bugs.json") as file:
            bugs = json.load(file)

        with open(config.DATA_DIR + "patches.json") as file:
            patches = json.load(file)

        for bug in bugs:
            if bug["name"] == kwargs["bug_name"]:
                break

        valid = True
        new_patch = True

        for patch in patches:
            if str(patch["id"]) in request.POST.keys():
                new_patch = False        

                break

        if not new_patch:
            if request.POST[str(patch["id"])] == "a":
                for patch_tag in patch["tags"]:
                    if patch_tag["tagId"] == int(request.POST["tag-id"]):
                        valid = False

                if valid:
                    patch["tags"].append({
                        "tagId": int(request.POST["tag-id"]),
                        "description": "",
                        "references": [{
                            "referenceId": 0,
                            "fieldNames": []
                        }]
                    })

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
        # contributor_name = request.POST['contributor']
        # patch_name = request.POST['name']
        # correctness = request.POST['correctness']
        # diff = request.FILES['diff'].read().decode("utf-8")

        with open(config.DATA_DIR + "patches.json", "w") as file:
            file.seek(0)
            file.write(json.dumps(patches))

        # else:
        #     if not 'labels' in patch:
        #         patch['labels'] = []

        #     patch['labels'].append(request.POST['tag-name-' + patch['id']])



        return redirect(reverse('dissection:bug-detail', kwargs={
            'bug_name':bug['name'], 
        }))

class PatchComparison(View):
    template_name = "patch-comparison.html"

    def get(self, request, *args, **kwargs):    
        with open(config.DATA_DIR + "bugs.json") as file:
            bugs = json.load(file)

        with open(config.DATA_DIR + "patches.json") as file:
            patches = json.load(file)

        with open(config.DATA_DIR + "tags.json") as file:
            tags = json.load(file)

        for bug in bugs:
            if bug['name'] == kwargs['bug_name']:
                break

        selected_patches = []

        for patch_id in kwargs["selected_patches"].split(","):
            selected_patches.append(query.get_object_by_id(patches, int(patch_id)))

        return render(request, self.template_name, {
            "bug": bug, 
            "patches": selected_patches,
            "tags": tags,
        })
    
    def post(self, request, *args, **kwargs):
        with open(config.DATA_DIR + "bugs.json") as file:
            bugs = json.load(file)

        with open(config.DATA_DIR + "patches.json") as file:
            patches = json.load(file)

        for bug in bugs:
            if bug["name"] == kwargs["bug_name"]:
                break

        valid = True

        for patch in patches:
            if str(patch["id"]) in request.POST.keys():
                break

        if request.POST[str(patch["id"])] == "a":
            for patch_tag in patch["tags"]:
                if patch_tag["tagId"] == int(request.POST["tag-id"]):
                    valid = False

            if valid:
                patch["tags"].append({
                    "tagId": int(request.POST["tag-id"]),
                    "description": "",
                    "references": [{
                        "referenceId": 0,
                        "fieldNames": []
                    }]
                })

        with open(config.DATA_DIR + "patches.json", "w") as file:
            file.seek(0)
            file.write(json.dumps(patches))

        return redirect(reverse('dissection:patch-comparison', kwargs={
            'bug_name': kwargs["bug_name"], 
            'selected_patches': kwargs["selected_patches"], 
        }))