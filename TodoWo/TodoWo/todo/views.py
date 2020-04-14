from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone


def singupuser(request):
    if request.method == "GET":
        return render(request, 'todo/signup.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('loggedIn')
            except IntegrityError:
                return render(request, 'todo/signup.html',
                              {'form': UserCreationForm(), 'error': 'Username not available'})
        else:
            return render(request, 'todo/signup.html', {'form': UserCreationForm(), 'error': 'Password did not match'})


def currenttodo(request):
    todos = Todo.objects.filter(user=request.user, dateCompleted__isnull=True)
    return render(request, 'todo/loggedIn.html', {'todos': todos })


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def home(request):
    return render(request, 'todo/home.html')


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html',
                          {'form': AuthenticationForm(), 'error': 'Username or password did not match'})
        else:
            login(request, user)
            return redirect('loggedIn')


def createtodo(request):
    if request.method == "GET":
        return render(request, 'todo/createtodo.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('loggedIn')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form': TodoForm(), 'error': 'Field limit Exceed'})


def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('loggedIn')
        except ValueError:
            return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form, 'error': 'Field Limit Exceed'})


def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == "POST":
        todo.dateCompleted = timezone.now()
        todo.save()
        return redirect('loggedIn')
    

def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method =="POST":
        todo.delete()
        return redirect('completetodo')