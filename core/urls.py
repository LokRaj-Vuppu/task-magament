from django.urls import path

from core.views import CreateTask, DeleteTask, GetAllTasks, UpdateTask, home

urlpatterns = [
    path("", home, name="home"),
    path("get/", GetAllTasks.as_view(), name="get_tasks"),
    path("create/", CreateTask.as_view(), name="create_task"),
    path("update/", UpdateTask.as_view(), name="update_task"),
    path("delete/", DeleteTask.as_view(), name="delete_task"),
]
