from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def home(request):
  return render(request, 'todo/home.html')


#Регистрация пользователя
def signupuser(request):
  # Вход на форму 
  if request.method == "GET":
    return render(request, 'todo/signupuser.html', {'form' : UserCreationForm()})

  # Если пароли не совпадают - остаемся на форме, добавив сообщение об ошибке  
  if request.POST['password1'] != request.POST['password2']:
    return render(request, 'todo/signupuser.html', {'form' : UserCreationForm(), 'error' : "Passwords didn't match"})

  # Создание пользователя и сохранение
  try:
    user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
    user.save()
    login(request, user)
    return redirect('currenttodos')
  except IntegrityError:
    return render(request, 'todo/signupuser.html',
                  {'form' : UserCreationForm(), 'error' : "That user has already been taken."})


# Вход пользователя
def loginuser(request):
  # Вход на форму 
  if request.method == "GET":
    return render(request, 'todo/loginuser.html', {'form' : AuthenticationForm()})

  user = authenticate(request, username=request.POST['username'], password=request.POST['password'])

  if user is None:
    return render(request, 'todo/loginuser.html', {'form' : AuthenticationForm(),
                                                   'error' : 'Username and password did not match'})
  login(request, user)
  return redirect('currenttodos')


# Выход пользователя
@login_required
def logoutuser(request):
  if request.method == "POST":
    logout(request)
    return redirect('home')


# Создание и сохранение задачи
@login_required
def createtodo(request):
  if request.method == "GET":
    return render(request, 'todo/createtodo.html', {'form' : TodoForm()})
  
  try:
    form = TodoForm(request.POST)
    newtodo = form.save(commit=False)
    newtodo.user = request.user
    newtodo.save()

    return redirect('currenttodos')

  except ValueError:
    return redirect('currenttodos', {'form' : TodoForm(), 'error':'Bad data passed. Try is again.'})


# Список всех задач текущего пользователя
@login_required
def currenttodos(request):
  todos = Todo.objects.filter(user=request.user, date_complete__isnull=True).order_by('-date_created')
  return render(request, 'todo/currenttodos.html', {'todos':todos})


# Список завершенных задач текущего пользователя
@login_required
def completedtodos(request):
  todos = Todo.objects.filter(user=request.user, date_complete__isnull=False).order_by('-date_complete')
  return render(request, 'todo/completetodos.html', {'todos':todos})


#Просмотр и редактирование задачи
@login_required
def viewtodo(request, todo_pk):
  todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)

  if request.method == "GET":
    form = TodoForm(instance=todo)
    return render(request, 'todo/viewtodo.html', {'form' : form, 'todo' : todo})

  try:
    form = TodoForm(request.POST, instance=todo)
    form.save()
    return redirect('currenttodos')
  except ValueError:
    return render(request, 'todo/viewtodo.html', {'form' : form, 'error': 'Bad info'})


#Функция завершения задачи
@login_required
def completetodo(request, todo_pk):
  todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)

  if request.method == "POST":
    todo.date_complete = timezone.now()
    todo.save()
    return redirect('currenttodos')


#Функция удаления задачи
@login_required
def deletetodo(request, todo_pk):
  todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)

  if request.method == "POST":
    todo.delete()
    return redirect('currenttodos')