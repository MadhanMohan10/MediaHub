from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('login/',views.login_process, name="loginPage"),
    path('signup/',views.registerPage, name="registerPage"),
    path('logout/', views.logoutuser, name="logout"),
]

