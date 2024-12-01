from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import CreateTaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required #Proteger los path para que solo entren usuarios logeados

# Create your views here.

def signUp(request):
    if request.method == 'GET':
        form = UserCreationForm
        return render(request, 'signup.html', {
            'form': form,
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1']) 
                user.save()
                login(request, user) # autenticar el usuario (mediante cookies)
                return redirect('tasks')
            except IntegrityError: #Cuando un usuario se repite en la base de datos
                return render(request, 'signup.html', {
                    'form': form,
                    'error': 'Username already exists'
                })
        return render(request, 'signup.html', {
            'form': form,
            'error': 'Password do not match'
        })
def home (request):
    return render(request, 'home.html')

@login_required
def tasks (request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render (request, 'tasks.html', {
        'tasks': tasks	
    })
    
@login_required
def tasks_completed (request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render (request, 'tasks.html', {
        'tasks': tasks    
    })

@login_required
def task_detail (request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk = task_id, user = request.user)
        form = CreateTaskForm(instance=task) # llena el formulario con la propiedad instance y la tarea
        return render(request, 'task_detail.html', {
            'task': task,
            'form': form
        })
    else:
        try:
            task = get_object_or_404(Task, pk= task_id, user = request.user)
            form = CreateTaskForm(request.POST, instance=task)
            form.save()
            return redirect ('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {
                'task': task,
                'form': form,
                'error': 'Error updating task'
            })

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')
    
@login_required
def delete_task (request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

@login_required
def signout (request):
    logout(request)
    return redirect('home')

def signin (request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        #Authenticate verifica si el usuario existe
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Username or password is incorrect'
            })
        else:
            login(request, user) #Guarda la sesion
            return redirect('tasks')
        
@login_required
def create_task (request):
    
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': CreateTaskForm
        })
    else:
        try:
            form = CreateTaskForm(request.POST)
            newTask = form.save(commit=False)
            newTask.user = request.user
            newTask.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
                'form': CreateTaskForm,
                'error': 'Error creating task'
            })