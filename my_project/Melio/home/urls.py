from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="home"),
    path("task_list/", task_list, name="task_list"),
    path("create_task_list/", create_task_list, name="create_task_list"),
    # path("update_task_list/", update_task_list, name="update_task_list"),
    path("delete_task_list/<int:pk>", delete_task_list, name="delete_task_list"),
    path(
        "manage_list_tasks/<int:task_list_id>",
        manage_list_tasks,
        name="manage_list_tasks",
    ),
    path("create_task/<int:pk>", create_task, name="create_task"),
    # path("update_task/", update_task, name="update_task"),
    path("delete_task/<int:pk>", delete_task, name="delete_task"),
    path("task_details/<int:pk>", task_details, name="task_details"),
]
