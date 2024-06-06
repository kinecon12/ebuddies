from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.loginview, name="loginpage"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="register"),
    
    path('', views.homepage, name='Homepage' ),
    path('home/', views.Home, name='Home'),
    path('room/<str:pk>', views.room, name='room'),
    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>', views.deleteRoom, name="delete-room"),
    
    
]
