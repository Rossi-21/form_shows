from django.urls import path
from . import views

urlpatterns = [

    path('', views.createShow, name="createShow"),
    path('shows/', views.dashboard, name="dashboard"),
    path('shows/<int:id>/', views.showShow, name="showShow"),
    path('shows/<int:id>/edit/', views.updateShow, name="updateShow"),
    path('shows/<int:id>/delete/', views.deleteShow, name="deleteShow" ),
    path('register', views.registerUser, name="registerUser"),
    path('user/<int:id>/', views.showUser, name="showUser"),
    path('user/<int:id>/update', views.updateUser, name="updateUser"),
    path('user/<int:id>/delete', views.deleteUser, name="deleteUser"),
    path('user/<int:id>/updateimage', views.updateImage, name="updateImage"),
    path('like/<int:id>/', views.likeShow, name="likeShow"),
    path('comment/<int:id>/delete', views.deleteComment, name="deleteComment"),
    path('login', views.loginUser, name="loginUser"),
    path('logout/', views.logoutUser, name="logout"),
]