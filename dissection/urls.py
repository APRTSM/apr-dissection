from django.urls import path
from . import views


app_name = 'dissection'

urlpatterns = [
    path("", views.BugsList.as_view(), name="bug-list"),
    path("<bug_name>/", views.BugDetail.as_view(), name="bug-detail"),
]
