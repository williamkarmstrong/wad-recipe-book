from recipes.forms import CommentForm, RecipeForm, UserForm, UserProfileForm
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from recipes.models import Category, Recipe

# Create your views here.

def index(request):
    context_dict = {}
    return render(request, 'recipes/index.html', context=context_dict)

  
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
        
    return render(request, 'signup.html', context = {'user_form' : user_form, 'profile_form' : profile_form, 'registered' : registered})

def category_view(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Recipe.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'recipes/category.html', context=context_dict)


def recipe_detail_view(request, category_slug, recipe_slug):
    recipe = Recipe.objects.get(title=recipe_slug)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})

  
def add_recipe_view(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.title = recipe.title
            recipe.save()
            return redirect('/')
    else:
        form = RecipeForm()
    return render(request, 'recipes/add_recipe.html', {'form': form})

  
def edit_recipe_view(request, category_slug, recipe_slug):
    recipe = Recipe.objects.get(title=recipe_slug)
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'recipes/edit_recipe.html', {'form': form})

  
def delete_recipe_view(request, category_slug, recipe_slug):
    recipe = Recipe.objects.get(title=recipe_slug)
    if request.method == 'POST':
        recipe.delete()
        return redirect('/')
    return render(request, 'recipes/delete_recipe.html', {'recipe': recipe})

  
def comment_view(request, category_slug, recipe_slug):
    recipe = Recipe.objects.get(title=recipe_slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.recipe = recipe
            comment.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))
  
  
def rate_recipe_view(request, recipe_slug):
    recipe = Recipe.objects.get(title=recipe_slug)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        if rating:
            recipe.ratings.add(rating)
    return redirect(request.META.get('HTTP_REFERER', '/'))

def save_recipe_view(request, recipe_slug):
    pass


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
