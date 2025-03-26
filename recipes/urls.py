from django.urls import path
from recipes import views

app_name = 'recipes'

urlpatterns = [
    path('', views.index, name='index'),
    path('categories/<slug:category_name_slug>/', views.category_view, name='category'),
    path('categories/<slug:category_name_slug>/<slug:recipe_slug>/', views.recipe_detail_view, name='recipe_detail'),
    path('add-recipe/', views.add_recipe_view, name='add_recipe'),
    path('categories/<slug:category_name_slug>/<slug:recipe_slug>/edit/', views.edit_recipe_view, name='edit_recipe'),
    path('categories/<slug:category_name_slug>/<slug:recipe_slug>/delete/', views.delete_recipe_view, name='delete_recipe'),
    path('categories/<slug:category_name_slug>/<slug:recipe_slug>/comment/', views.comment_view, name='comment'),
    path('categories/<slug:category_name_slug>/<slug:recipe_slug>/rate/', views.rate_recipe_view, name='rate'),
    path('categories/<slug:category_name_slug>/<slug:recipe_slug>/save/', views.save_recipe_view, name='save'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('restricted/', views.restricted, name='restricted'),
    path('logout/', views.user_logout, name='logout'),
]
