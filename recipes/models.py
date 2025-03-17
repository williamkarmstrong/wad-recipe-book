from django.db import models
<<<<<<< HEAD
from django.db.models import Q
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.
class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",  
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions_set",  
        blank=True
    )

class Recipe(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="recipes")
    ingredients = models.TextField()  # To save json type ingredients
    prep_time = models.IntegerField(help_text="Preparation time in minutes")
    difficulty = models.CharField(max_length=20, choices=[("Easy", "Easy"), ("Medium", "Medium"), ("Hard", "Hard")])
    created_at = models.DateTimeField(auto_now_add=True)

class SavedRecipe(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="saved_recipes")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="saved_by_users")
    saved_at = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)

class Rating(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="ratings")
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    rated_at = models.DateTimeField(auto_now=True)

def search_recipes(request):
    query = request.GET.get("q", "")
    recipes = Recipe.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    return JsonResponse(list(recipes.values()), safe=False)
=======
from django.contrib.auth.models import User

class UserProfile(models.Model):
    
    user = models.OneToOneField(User, on_delete = models.CASCADE)
     
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    
    def __str__(self):
        return self.user.username
>>>>>>> 0ca6aef9f867ef252753566db911bd1e3eaaa691
