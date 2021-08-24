"""todowoo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin, auth
from django.urls import path
from todo import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),

    # Auth
    path('signup/', views.signupuser, name='signupuser'),
    path('login/', views.loginuser, name='loginuser'),
    path('logout/', views.logoutuser, name='logoutuser'),

    # Todo create
    path('create/', views.createtodo, name='createtodo'),
    # Todo list all
    path('current/', views.currenttodos, name='currenttodos'),
    # Todo list completed
    path('completed/', views.completedtodos, name='completedtodos'),
    # Todo view current
    path('todo/<int:todo_pk>', views.viewtodo, name='viewtodo'),
    # Finished todos
    path('todo/<int:todo_pk>/complete', views.completetodo, name='completetodo'),
    # Deleting the record
    path('todo/<int:todo_pk>/delete', views.deletetodo, name='deletetodo'),
]