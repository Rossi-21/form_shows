from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name="home"),
    path('shows/', views.allShows, name="allShows"),
    path('shows/<int:id>/', views.viewShow, name="viewShow"),
    path('shows/<int:id>/edit/', views.editShow, name="editShow"),
    path('shows/<int:id>/delete/', views.deleteShow, name="deleteShow" ),
    path('register', views.registerUser, name="registerUser"),
    path('user/<int:id>/', views.showUser, name="showUser"),
    path('like/<int:id>/', views.likeShow, name="likeShow"),
    path('comment/<int:id>/', views.commentShow, name="commentShow"),
    path('login', views.loginUser, name="loginUser"),
    path('logout/', views.logoutUser, name="logoutUser"),
]