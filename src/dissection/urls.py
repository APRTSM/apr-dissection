from django.urls import path
from .utils import config
from . import views


app_name = config.APP_NAME

urlpatterns = [
    path("", views.BugsList.as_view(), name="bug-list"),
    path("<bug_name>/", views.BugDetail.as_view(), name="bug-detail"),
    path("<bug_name>/<selected_patches>/", views.PatchComparison.as_view(), name="patch-comparison"),
]
