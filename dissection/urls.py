from django.urls import path
from . import views


app_name = 'dissection'

urlpatterns = [
    path("", views.BugsList.as_view(), name="bug-list"),
    path("<bug_project>/<int:bug_id>/", views.BugDetail.as_view(), name="bug-detail"),
]
