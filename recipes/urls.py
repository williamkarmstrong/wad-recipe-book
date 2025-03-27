from django.urls import path
from recipes import views
from .views import my_recipes_view

app_name = 'recipes'

urlpatterns = [
    path('', views.index, name='index'),
    path('categories/<slug:category_name_slug>/', views.category_view, name='category'),
    path('<int:recipe_id>/', views.recipe_detail_view, name='recipe_detail'),
    path('add-recipe/', views.add_recipe_view, name='add_recipe'),
    path('<int:recipe_id>/edit/', views.edit_recipe_view, name='edit_recipe'),
    path('<int:recipe_id>/delete/', views.delete_recipe_view, name='delete_recipe'),
    path('<int:recipe_id>/comment/', views.comment_view, name='comment'),
    path('<int:recipe_id>/rate/', views.rate_recipe_view, name='rate'),
    path('<int:recipe_id>/save/', views.save_recipe_view, name='save'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('restricted/', views.restricted, name='restricted'),
    path('logout/', views.user_logout, name='logout'),
    path('myrecipes/', my_recipes_view, name='myrecipes'),
]
