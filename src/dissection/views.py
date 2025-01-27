import json
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from django.urls import reverse
from .utils import config, query
from django.http import HttpResponseRedirect


class IndexView(TemplateView):
    template_name = "index.html"
    

class HomeView(TemplateView):
    template_name = "home.html"

    def post(self, request, *args, **kwargs):
        input_id = request.POST.get("id")

        if input_id:
            request.session["user_id"] = input_id

            return redirect(reverse("dissection:comparison", kwargs={"tool_patch_index": "0"}))

        return HttpResponseRedirect(request.path)


class ComparisonView(View):
    template_name = "comparison.html"

    def get(self, request, *args, **kwargs):
        tool_patch_index = kwargs.get("tool_patch_index")

        all_developer_patches = query.get_all("cleaned-developer-patches.pkl")
        all_tool_patches = query.get_all("cleaned-tool-patches.pkl")

        all_correct_tool_patches = all_tool_patches[all_tool_patches["correctness"] == "Correct"]

        tool_patch = all_correct_tool_patches.iloc[int(tool_patch_index)]
        developer_patch = all_developer_patches[all_developer_patches["bug_uid"] == tool_patch["bug_uid"]].iloc[0]

        developer_diff = query.read_file(f"{developer_patch.name}.patch")
        tool_patch_diff = query.read_file(f"{tool_patch.name}.patch")

        return render(request, self.template_name, {
            "bug_uid": tool_patch["bug_uid"],
            "tool_patch_index": tool_patch_index,
            "developer_patch_name": developer_patch.name, 
            "tool_patch_name": tool_patch.name, 
            "developer_diff": developer_diff, 
            "tool_patch_diff": tool_patch_diff,
            "tool_patch_expert_label": tool_patch["expert_label"],
        })

    def post(self, request, *args, **kwargs):
        tool_patch_index = int(kwargs.get("tool_patch_index"))
        expert_label = request.POST.get("type")

        all_tool_patches = query.get_all("cleaned-tool-patches.pkl")
        all_correct_tool_patches = all_tool_patches[all_tool_patches["correctness"] == "Correct"]

        tool_patch = all_correct_tool_patches.iloc[int(tool_patch_index)]
        all_tool_patches.at[tool_patch.name, "expert_label"] = expert_label


        print(expert_label)
        print(all_correct_tool_patches)
        print(all_correct_tool_patches.iloc[int(tool_patch_index)])
        query.save("cleaned-tool-patches.pkl", all_tool_patches)

        next_tool_patch_index = tool_patch_index + 1

        return redirect(reverse("dissection:comparison", kwargs={"tool_patch_index": next_tool_patch_index}))


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
