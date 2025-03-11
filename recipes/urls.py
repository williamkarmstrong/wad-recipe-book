from django.urls import path
from recipes import views

app_name = 'recipes'

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.register, name='signup'),
    path('login/', views.user_login, name='login'),
    path('restricted/', views.restricted, name='restricted'),
    path('logout/', views.user_logout, name='logout'),
]
