from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import TaskList, Task
from .forms import TaskListForm, TaskForm


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect("task_list")
    return render(request, "home/index.html")


@login_required
def task_list(request):
    task_lists = TaskList.objects.filter(user=request.user)
    return render(request, "home/index2.html", {"task_lists": task_lists})


@login_required
def create_task_list(request):
    if request.method == "POST":
        form = TaskListForm(request.POST)
        if form.is_valid():
            task_list = form.save(commit=False)
            task_list.user = request.user
            task_list.save()
            return redirect("task_list")
    else:
        form = TaskListForm()
    return render(request, "home/index3.html", {"form": form})


@login_required
def delete_task_list(request, pk):
    task_list = get_object_or_404(TaskList, pk=pk)
    if task_list.user == request.user:
        task_list.delete()
    return redirect("task_list")


@login_required
def manage_list_tasks(request, task_list_id):
    task_list = get_object_or_404(TaskList, id=task_list_id)
    tasks = Task.objects.filter(task_list=task_list)
    context = {
        "task_list": task_list,
        "tasks": tasks,
    }
    return render(request, "home/index4.html", context)


@login_required
def create_task(request, pk):
    if request.method == "POST":
        task_list = get_object_or_404(TaskList, pk=pk)
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.task_list = task_list
            task.save()
            return redirect("task_list")
    else:
        form = TaskForm()
    return render(request, "home/index5.html", {"form": form})


@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if task.task_list.user == request.user:
        task.delete()
    return redirect("task_list")


@login_required
def task_details(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task_list = task.task_list.name
    context = {
        "task": task,
        "task_list": task_list,
    }
    return render(request, "home/index6.html", context)
