from django.urls import path
from .utils import config
from . import views


app_name = config.APP_NAME

urlpatterns = [
    path("bugs/", views.BugListView.as_view(), name="bug-list"),
    path("bugs/<name>/", views.BugDetailView.as_view(), name="bug-detail"),
    path("bugs/<name>/<patches>/", views.PatchComparisonView.as_view(), name="patch-comparison"),
    path("tags/", views.TagListView.as_view(), name="tag-list"),
    path("tags/new/", views.TagNewView.as_view(), name="tag-new"),

]
