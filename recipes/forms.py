from django import forms 
from django.contrib.auth.models import User
from recipes.models import Rating, Recipe, UserProfile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta: 
        model = User
        fields = ('username', 'email', 'password',)
        
class UserProfileForm(forms.ModelForm): 
    class Meta:
        model = UserProfile
        fields = ('website', 'picture',)


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'image', 'difficulty', 'category', 'description', 'ingredients', 'instructions']
        
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'ingredients': forms.Textarea(attrs={'rows': 3}),
            'instructions': forms.Textarea(attrs={'rows': 5}),
            'difficulty': forms.Select(choices=Recipe.DIFFICULTY_CHOICES),
        }


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ["rating"]  # Only allow selecting a rating (1-5)

# class RecipeForm(forms.ModelForm):
#     title = forms.CharField(max_length=128, help_text="Please enter the title of the page.")
#     picture = forms.ImageField()
#     description = forms.CharField(max_length=255, help_text="Please enter a description")
#     prep_time = forms.IntegerField(max_value=100, help_text="Preparation time in minutes")
#     difficulty = forms.ChoiceField()
#     ingredients = forms.CharField()
#     instructions = forms.Textarea()

#     class Meta:
#         model = Recipe
#         exclude = ('author', 'category','created_at', 'rating', 'slug')

class CommentForm(forms.ModelForm):
    pass

