from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name="home"),
    path('shows/', views.allShows, name="allShows"),
    path('shows/<int:id>/', views.viewShow, name="viewShow"),
    path('shows/<int:id>/edit/', views.editShow, name="editShow"),
    path('shows/<int:id>/delete/', views.deleteShow, name="deleteShow" ),
    #path('register', views.registerPage, name="register"),
    #path('login', views.loginPage, name="login"),
    #path('logout/', views.logoutUser, name="logout"),

]