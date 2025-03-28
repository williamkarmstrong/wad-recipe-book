from recipes.forms import CommentForm, RatingForm, RecipeForm, UserForm, UserProfileForm
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from recipes.models import Category, Rating, Recipe
from datetime import datetime
from django.http import JsonResponse
from recipes.models import Recipe, SavedRecipe
from .forms import CategoryForm

# Create your views here.

def index(request):
    context = get_categories()
    return render(request, 'recipes/index.html', context=context)

def get_categories():
    context_dict = {}
    try:
        categories = Category.objects.all() 
        context_dict['categories'] = categories
    except Category.DoesNotExist:
        context_dict['categories'] = None
    return context_dict



@login_required
def add_category_view(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('recipes:myrecipes')  
    else:
        form = CategoryForm()
    return render(request, 'recipes/add_category.html', {'form': form})

def category_view(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Recipe.objects.filter(category=category)
        context_dict['recipes'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['recipes'] = None

    return render(request, 'recipes/category.html', context=context_dict)


def recipe_detail_view(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    return render(request, 'recipes/recipe.html', {'recipe': recipe})

  
def add_recipe_view(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            return redirect('/')
    else:
        form = RecipeForm()
    return render(request, 'recipes/addrecipe.html', {'form': form})

  
def edit_recipe_view(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    if recipe.author != request.user:
        return HttpResponseForbidden("You are not allowed to edit this recipe.")
    
    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return render(request, "recipes/recipe.html", {"recipe": recipe})
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'recipes/editrecipe.html', {'form': form, 'recipe': recipe})

  
def delete_recipe_view(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    if request.method == 'POST':
        recipe.delete()
        return redirect('/')
    return render(request, 'recipes/deleterecipe.html', {'recipe': recipe})

  
def comment_view(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.recipe = recipe
            comment.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))
  
  
@login_required
def rate_recipe_view(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    rating_instance = Rating.objects.filter(user=request.user, recipe=recipe).first()

    if request.method == "POST":
        form = RatingForm(request.POST, instance=rating_instance)  # Use existing rating if it exists
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = request.user
            rating.recipe = recipe
            rating.save()
            return render(request, 'recipes/recipe.html', {'recipe': recipe})

    else:
        form = RatingForm(instance=rating_instance)

    return render(request, "recipes/raterecipe.html", {"form": form, "recipe": recipe})

@login_required
def my_recipes_view(request):
    saved_recipes = SavedRecipe.objects.filter(user=request.user).select_related('recipe')
    recipes = [saved.recipe for saved in saved_recipes]
    context = {'recipes': recipes}
    return render(request, 'recipes/myrecipes.html', context)

@login_required
def save_recipe_view(request, recipe_id):
    if request.method == "POST":
        try:
            recipe = Recipe.objects.get(id=recipe_id)
            saved_recipe = SavedRecipe.objects.filter(user=request.user, recipe=recipe).first()
            if saved_recipe:
                saved_recipe.delete()
                return JsonResponse({"unsaved": True})
            else:
                SavedRecipe.objects.create(user=request.user, recipe=recipe)
                return JsonResponse({"saved": True})
        except Recipe.DoesNotExist:
            return JsonResponse({"error": "Recipe not found."}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method."}, status=400)

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'recipes/register.html', context={'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

  
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
  
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('recipes:index'))
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'recipes/login.html')
    
    
def some_view(request):
    if not request.user.is_authenticated():
        return HttpResponse("You are logged in.") 
    else:
        return HttpResponse("You are not logged in.")

      
@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")
  

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('recipes:index'))