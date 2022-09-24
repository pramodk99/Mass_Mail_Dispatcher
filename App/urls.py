from django.contrib import admin
from django.urls import path 
from App import views 
urlpatterns = [
    path("",views.home, name="home"),
    path("index", views.index, name="App"),
    path("login", views.loginUser, name="login"),
    path("logout", views.logoutUser, name="logout"),
    path("about", views.about, name="about"),
    path("signup", views.signup, name="signup"),
    path("send", views.emails, name="emails"),
    path("file", views.file, name="file"),
    path("validate", views.validate, name="validate"),
    path("check_username", views.check_username, name="check_username"),
    path("invalid", views.invalid, name="invalid")

]
