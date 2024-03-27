import json
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from django.urls import reverse
from .utils import config, query


class IndexView(TemplateView):
    template_name = "index.html"
    

class BugListView(View):
    template_name = "bug-list.html"

    def get(self, request, *args, **kwargs):    
        bugs = query.get_all("bugs.json")
        patches = query.get_all("patches.json")
        benchmarks = query.get_all("benchmarks.json")

        return render(request, self.template_name, {"bugs": bugs, "benchmarks": benchmarks, "patches": patches, "title": "List of Bugs"})


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
            'name':bug['name'], 
        }))

class PatchComparisonView(View):
    template_name = "patch-comparison.html"

    def get(self, request, *args, **kwargs):    
        references = query.get_all("references.json")
        bugs = query.get_all("bugs.json")
        patches = query.get_all("patches.json")  
        tags = query.get_all("tags.json")
        comments = query.get_all("comments.json")

        patch_comment_pairs = query.get_foreign_key_pairs(comments, "patchId")

        bug = query.get_object_by_unique_feature(bugs, "name", kwargs["name"])
        selected_patches = [query.get_object_by_id(patches, int(patch_id)) for patch_id in kwargs["patches"].split(",")]

        return render(request, self.template_name, {
            "references": references,
            "bug": bug, 
            "patches": selected_patches,
            "tags": tags,
            "comments": comments,
            "patch_comment_pairs": patch_comment_pairs,
        })
    
    def post(self, request, *args, **kwargs):
        bugs = query.get_all("bugs.json")
        patches = query.get_all("patches.json")    
        comments = query.get_all("comments.json")    
        bug = query.get_objects_by_feature(bugs, "name", kwargs['name'])[0]

        for patch in patches:
            if str(patch["id"]) + "-add-comment" in request.POST.keys():
                break

        new_comment = {
            "id": len(comments) + 1,
            "patchId": patch["id"],
            "content": request.POST["comment-content"],
            "followingCommentId": 0,
            "referenceId": 1,
        }

        comments.append(new_comment)

        query.commit("comments.json", comments)

        return redirect(reverse("dissection:patch-comparison", kwargs={
            "name":kwargs["name"], 
            "patches": kwargs["patches"],
        }))
    
class PatchExportView(View):
    def post(self, request, *args, **kwargs):    
        patches = query.get_all("patches.json")  
        patch = query.get_object_by_id(patches, int(kwargs["patch_id"]))
        kwargs["name"] + patch["tool"] + patch["id"]
        


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
