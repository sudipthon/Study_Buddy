from django.urls import path
from . import views

urlpatterns=[
    path('login/',views.Log,name='login_page'),
    path('logout/',views.LogOutUser,name='logout_page'),
    path('register/',views.RegisterUser,name='register_page'),
    path('',views.rooms,name='rooms'),
    path('room/<str:pk>/',views.room,name='room'),
    path('profile/<str:pk>/',views.UserProfile,name='profile'),
    path('create/',views.createRoom,name='create-room'),
    path('update/<str:pk>/',views.updateRoom,name='update-room'),
    path('delete/<str:pk>/',views.DeleteRoom,name='delete-room'),
    path('delete-message/<str:pk>/',views.DeleteMessage,name='delete-message'),
    path('update-user/',views.UpdateUser,name='UpdateUser'),
    path('topics/',views.TopicResponsive,name='TopicResponsive'),
    path('activity/',views.ActivityResponsive,name='ActivityResponsive'),

]