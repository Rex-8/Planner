from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from itertools import chain
from .models import ToDoList, Notes, Task

def handle_post_actions(request):
    for key in request.POST:
        if key.startswith('del'):
            slug = key.replace('del', '')
            content = get_object_or_404(Notes, slug=slug, user=request.user) if 'n' in slug else get_object_or_404(ToDoList, slug=slug, user=request.user)
            content.delete()
        elif key.startswith('fav'):
            slug = key.replace('fav', '')
            content = get_object_or_404(Notes, slug=slug, user=request.user) if 'n' in slug else get_object_or_404(ToDoList, slug=slug, user=request.user)
            content.favourite = True
            content.save()
        elif key.startswith('unfav'):
            slug = key.replace('unfav', '')
            content = get_object_or_404(Notes, slug=slug, user=request.user) if 'n' in slug else get_object_or_404(ToDoList, slug=slug, user=request.user)
            content.favourite = False
            content.save()

@login_required(login_url='User:login')
def home(request):
    if request.method == 'POST':
        handle_post_actions(request)
        return redirect('Content:home')

    t = ToDoList.objects.filter(user=request.user)
    n = Notes.objects.filter(user=request.user)
    contents = sorted(chain(t, n), key=lambda instance: instance.date, reverse=True)
    return render(request, 'content_list.html', {
        'page_title': 'Organiser',
        'page_heading': 'Recent',
        'contents': contents
    })

@login_required(login_url='User:login')
def favs(request):
    if request.method == 'POST':
        handle_post_actions(request)
        return redirect('Content:favs')

    t = ToDoList.objects.filter(favourite=True, user=request.user)
    n = Notes.objects.filter(favourite=True, user=request.user)
    favourites = chain(t, n)
    return render(request, 'content_list.html', {
        'page_title': 'Favs',
        'page_heading': 'Favourites',
        'contents': favourites
    })

@login_required(login_url='User:login')
def notes(request):
    if request.method == 'POST':
        handle_post_actions(request)
        return redirect('Content:notes')

    contents = Notes.objects.filter(user=request.user)
    return render(request, 'content_list.html', {
        'page_title': 'Notes',
        'page_heading': 'Notes',
        'contents': contents
    })

@login_required(login_url='User:login')
def todolists(request):
    if request.method == 'POST':
        handle_post_actions(request)
        return redirect('Content:todolists')

    contents = ToDoList.objects.filter(user=request.user)
    return render(request, 'content_list.html', {
        'page_title': 'To do list',
        'page_heading': 'To do lists',
        'contents': contents
    })

@login_required(login_url='User:login')
def view_content(request, slug):
    todo_lists = ToDoList.objects.filter(user=request.user)
    notes = Notes.objects.filter(user=request.user)
    contents = chain(todo_lists, notes)
    
    content = next((item for item in contents if item.slug == slug), None)
    
    if not content:
        return HttpResponse("Content not found", status=404)

    if request.method == 'POST':
        new_title = request.POST.get('content-heading')
        if new_title:
            content.title = new_title

        if isinstance(content, Notes):
            if 'note-body' in request.POST:
                content.body = request.POST.get('note-body')

            for key in request.POST:
                if key.startswith('fav'):
                    content.favourite = True
                elif key.startswith('unfav'):
                    content.favourite = False
                elif key.startswith('del'):
                    content.delete()
                    return redirect('Content:home')
            
        elif isinstance(content, ToDoList):
            for task in content.tasks.all():
                task.completion = False
            for key in request.POST:
                if key.startswith('task-completion'):
                    task_id = key.replace('task-completion', '')
                    task = get_object_or_404(Task, id=task_id)
                    task.completion = True
                    task.save()
                
                elif key.startswith('task-body'):
                    task_id = key.replace('task-body', '')
                    task = get_object_or_404(Task, id=task_id)
                    value = request.POST[key]
                    if value == '':
                        task.delete()
                    else:
                        task.body = value
                        task.save()
                
                elif key.startswith('delete-task'):
                    task_id = key.replace('delete-task', '')
                    task = get_object_or_404(Task, id=task_id)
                    task.delete()
                
                elif key == 'add-task':
                    task_body = request.POST.get('add-body', '').strip()
                    if task_body:
                        Task.objects.create(body=task_body, to_do_list=content)
                
                elif key.startswith('fav'):
                    content.favourite = True
                elif key.startswith('unfav'):
                    content.favourite = False
                elif key.startswith('del'):
                    content.delete()
                    return redirect('Content:home')

        content.save()

    if isinstance(content, Notes):
        return render(request, 'view_note.html', {'content': content})
    elif isinstance(content, ToDoList):
        return render(request, 'view_todolist.html', {'content': content})

    return HttpResponse("Content not found", status=404)

def create_content(request):
    return render(request, 'create_content.html')

@login_required(login_url='User:login')
def create_note(request):
    note = Notes(title='Default Title', body='', user=request.user)
    note.save()
    note.slug = f'n{note.id}'
    note.save()
    return redirect('Content:content_page', slug=note.slug)

@login_required(login_url='User:login')
def create_todolist(request):
    todolist = ToDoList(title='Default Title', user=request.user)
    todolist.save()
    todolist.slug = f't{todolist.id}'
    todolist.save()
    return redirect('Content:content_page', slug=todolist.slug)
