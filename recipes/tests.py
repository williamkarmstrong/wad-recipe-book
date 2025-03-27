from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from recipes.forms import RecipeForm
from recipes.models import Recipe, Rating, Category



class AuthTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
    
    def test_register_user(self):
        response = self.client.post(reverse('recipes:register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword',
            'password_confirm': 'newpassword',
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_login_user(self):
        response = self.client.post(reverse('recipes:login'), {
            'username': 'testuser',
            'password': 'testpassword',
        })
        
        self.assertEqual(response.status_code, 302)  
        self.assertTrue('_auth_user_id' in self.client.session)
    
    def test_login_invalid_user(self):
        response = self.client.post(reverse('recipes:login'), {
            'username': 'wronguser',
            'password': 'wrongpassword',
        })
        
        self.assertEqual(response.status_code, 200)  
        self.assertFalse('_auth_user_id' in self.client.session)
    
    def test_logout_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('recipes:logout'))
        
        self.assertEqual(response.status_code, 302)  
        self.assertFalse('_auth_user_id' in self.client.session)



class RecipeFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.category = Category.objects.create(name="Desserts")

    def test_recipe_form_valid(self):
        form_data = {
            'title': 'Chocolate Cake',
            'category': self.category.id,  
            'description': 'A delicious chocolate cake.',
            'difficulty': 'Easy',
            'ingredients': 'Chocolate, flour, sugar, eggs',
            'instructions': 'Mix and bake.',
            'author': self.user.id 
        }
        
        form = RecipeForm(data=form_data)
        print(form.errors)
        self.assertTrue(form.is_valid())



class RecipeModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Dessert", slug="dessert")
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')
        
        self.recipe = Recipe.objects.create(
            title='Chocolate Cake',
            description='A delicious chocolate cake.',
            difficulty='Easy',
            ingredients='Chocolate, flour, eggs',
            instructions='Mix and bake.',
            author=self.user1,
            category=self.category,
        )

        Rating.objects.create(recipe=self.recipe, user=self.user1, rating=5)
        Rating.objects.create(recipe=self.recipe, user=self.user2, rating=3)

    def test_average_rating(self):
        average_rating = self.recipe.average_rating()
        expected_average = (5 + 3) / 2  
        
        self.assertEqual(average_rating, expected_average)

    def test_no_ratings(self):
        recipe_without_ratings = Recipe.objects.create(
            title='Vanilla Cake',
            description='A simple vanilla cake.',
            difficulty='Medium',
            ingredients='Flour, sugar, eggs',
            instructions='Mix and bake.',
            author=self.user1,
            category=self.category,
        )
        
        self.assertEqual(recipe_without_ratings.average_rating(), 0)
