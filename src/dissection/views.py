import json
from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
from .utils import config, query


class BugListView(View):
    template_name = "bug-list.html"

    def get(self, request, *args, **kwargs):    
        bugs = query.get_all("bugs.json")
        benchmarks = query.get_all("benchmarks.json")

        return render(request, self.template_name, {"bugs": bugs, "benchmarks": benchmarks, "title": "List of Bugs"})


class BugDetailView(View):
    template_name = "bug-detail.html"

    def get(self, request, *args, **kwargs):    
        bugs = query.get_all("bugs.json")
        patches = query.get_all("patches.json")
        tags = query.get_all("tags.json")
        bug = query.get_objects_by_feature(bugs, "name", kwargs['name'])[0]
        selected_patches = query.get_objects_by_feature(patches, "bugId", bug["id"])

        return render(request, self.template_name, {
            "bug": bug, 
            "patches": selected_patches,
            "tags": tags,
        })
    
    def post(self, request, *args, **kwargs):
        bugs = query.get_all("bugs.json")
        patches = query.get_all("patches.json")    
        bug = query.get_objects_by_feature(bugs, "name", kwargs['name'])[0]
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

        query.commit("patches.json", patches)

        return redirect(reverse('dissection:bug-detail', kwargs={
            'bug_name':bug['name'], 
        }))

class PatchComparisonView(View):
    template_name = "patch-comparison.html"

    def get(self, request, *args, **kwargs):    
        bugs = query.get_all("bugs.json")
        patches = query.get_all("patches.json")  
        tags = query.get_all("tags.json")
        bug = query.get_objects_by_feature(bugs, "name", kwargs["name"])
        selected_patches = [query.get_object_by_id(patches, int(patch_id)) for patch_id in kwargs["patches"].split(",")]

        return render(request, self.template_name, {
            "bug": bug, 
            "patches": selected_patches,
            "tags": tags,
        })
    
        with open(config.DATA_DIR + "bugs.json") as file:
            bugs = json.load(file)

        with open(config.DATA_DIR + "patches.json") as file:
            patches = json.load(file)

        for bug in bugs:
            if bug["name"] == kwargs["name"]:
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
            'bug_name': kwargs["name"], 
            'selected_patches': kwargs["selected_patches"], 
        }))

class TagListView(View):
    template_name = "tag-list.html"

    def get(self, request, *args, **kwargs):    
        tags = query.get_all("tags.json")
        classes = query.get_all("classes.json")

        return render(request, self.template_name, {"tags": tags, "classes": classes})
    
class TagNewView(View):
    template_name = "tag-new.html"

    def get(self, request, *args, **kwargs):    
        tags = query.get_all("tags.json")
        classes = query.get_all("classes.json")

        return render(request, self.template_name, {"tags": tags, "classes": classes})
    
    def post(self, request, *args, **kwargs):
        tags = query.get_all("tags.json")
        classes = query.get_all("classes.json")
        value = request.POST["value"]
        references = [
            {
                "referenceId": 1,
                "fieldNames": [],
            }
        ]

        if not value:
            value = None

        new_tag = {
            "id": len(tags) + 1,
            "name": request.POST["name"],
            "classId": int(request.POST["classId"]),
            "value": value,
            "briefDescription": request.POST["briefDescription"],
            "description": request.POST["description"],
            "references": references,

        }

        query.add_object("tags.json", new_tag)

        return render(request, self.template_name, {"tags": tags, "classes": classes})
