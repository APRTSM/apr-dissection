from django.shortcuts import render
from django.views import View
from django.templatetags.static import static
import json
import urllib


class Home(View):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):    
        url = request.build_absolute_uri('/') + static('data/defects4j-bugs.json')
        
        with urllib.request.urlopen(url) as defects4j:
            defects = json.load(defects4j)

        url = request.build_absolute_uri('/') + static('data/classification.json')

        with urllib.request.urlopen(url) as defects4j:
            classes = json.load(defects4j)
        

        return render(request, self.template_name, {"defects": defects, "classes": classes})
