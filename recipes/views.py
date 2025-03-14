from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).days > 0:
        visits += 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie

    request.session['visits'] = visits

def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {
        'boldmessage': 'Homepage',
        'categories': category_list,
        'pages': page_list
    }
    visitor_cookie_handler(request)
    return render(request, 'recipes/index.html', context=context_dict)

def show_category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'recipes/category.html', context=context_dict)


def recipe_detail_view(request, category_slug, recipe_slug):
    recipe = get_object_or_404(Recipe, slug=recipe_slug)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})

def add_recipe_view(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.slug = slugify(recipe.title)
            recipe.save()
            return redirect('/')
    else:
        form = RecipeForm()
    return render(request, 'recipes/add_recipe.html', {'form': form})

def edit_recipe_view(request, category_slug, recipe_slug):
    recipe = get_object_or_404(Recipe, slug=recipe_slug)
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'recipes/edit_recipe.html', {'form': form})

def delete_recipe_view(request, category_slug, recipe_slug):
    recipe = get_object_or_404(Recipe, slug=recipe_slug)
    if request.method == 'POST':
        recipe.delete()
        return redirect('/')
    return render(request, 'recipes/delete_recipe.html', {'recipe': recipe})

def comment_view(request, category_slug, recipe_slug):
    recipe = get_object_or_404(Recipe, slug=recipe_slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.recipe = recipe
            comment.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))

def rate_view(request, category_slug, recipe_slug):
    recipe = get_object_or_404(Recipe, slug=recipe_slug)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        if rating:
            recipe.ratings.add(rating)
    return redirect(request.META.get('HTTP_REFERER', '/'))


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
                return HttpResponse("Your Recipes account is disabled.")
        else:
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'recipes/login.html')

@login_required
def restricted(request):
    return render(request, 'recipes/restricted.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('recipes:index'))
