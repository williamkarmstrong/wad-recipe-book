from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from recipes.forms import RecipeForm, RatingForm
from recipes.models import Recipe, Rating, Category
from recipes.models import SavedRecipe, Comment



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
    
    def test_register_existing_username(self):
        response = self.client.post(reverse('recipes:register'), {
            'username': 'testuser',
            'email': 'testuser2@example.com',
            'password': 'newpassword',
            'password_confirm': 'newpassword',
        })
        
        self.assertEqual(response.status_code, 200)  
        self.assertEqual(User.objects.filter(username='testuser').count(), 1)
        
    def test_login_without_password(self):
        response = self.client.post(reverse('recipes:login'), {
            'username': 'testuser',
            'password': '',
        })
        
        self.assertEqual(response.status_code, 200)  
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
        
        self.assertTrue(form.is_valid())
        
    def test_recipe_form_title_too_long(self):
        form_data = {
            "title": "A" * 300,
            "category": self.category.id,
            "description": "Test description",
            "difficulty": "Easy",
            "ingredients": "Test ingredients",
            "instructions": "Test instructions",
        }
        
        form = RecipeForm(data=form_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)



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
        
    def test_recipe_slug_creation(self):
        recipe = Recipe.objects.create(
            title="New Delicious Cake",
            description="Test description",
            difficulty="Easy",
            ingredients="Test ingredients",
            instructions="Test instructions",
            author=self.user1,
            category=self.category,
        )
        
        self.assertEqual(recipe.slug, "new-delicious-cake")
        
    def test_recipe_form_empty_description(self):
        form_data = {
            "title": "Test Cake",
            "category": self.category.id,
            "description": "",
            "difficulty": "Easy",
            "ingredients": "Flour, Sugar",
            "instructions": "Mix and bake",
        }
        
        form = RecipeForm(data=form_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn("description", form.errors)

      
      
class TemplateTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.category = Category.objects.create(name="Dessert", slug="dessert")

        self.recipe = Recipe.objects.create(
            title="Chocolate Cake",
            author=self.user,
            category=self.category,
            description="Delicious chocolate cake",
            difficulty="Medium",
            ingredients="Flour, Sugar, Cocoa",
            instructions="Mix and bake",
            slug="chocolate-cake"
        )

    def test_recipe_detail_template_used(self):
        response = self.client.get(reverse("recipes:recipe_detail", args=[self.recipe.id]))
        
        self.assertTemplateUsed(response, "recipes/recipe.html")

    def test_recipe_detail_context(self):
        response = self.client.get(reverse("recipes:recipe_detail", args=[self.recipe.id]))
        
        self.assertEqual(response.context["recipe"], self.recipe)

    def test_user_logged_in_state(self):
        response = self.client.get(reverse("recipes:index"))
        
        self.assertContains(response, "Login")  
        self.assertNotContains(response, "Logout") 

        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("recipes:index"))
        
        self.assertContains(response, "Logout")  
        self.assertNotContains(response, "Login") 
        


class FormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.category = Category.objects.create(name="Desserts", slug="desserts")

    def test_recipe_form_valid(self):
        form_data = {
            "title": "Chocolate Cake",
            "category": self.category.id,
            "description": "A delicious chocolate cake.",
            "difficulty": "Easy",
            "ingredients": "Chocolate, Flour, Sugar",
            "instructions": "Mix and bake.",
        }
        
        form = RecipeForm(data=form_data)
        
        self.assertTrue(form.is_valid())

    def test_recipe_form_invalid(self):
        form_data = {
            "title": "",  
            "category": "",
            "description": "No category",
            "difficulty": "Easy",
            "ingredients": "Chocolate, Flour, Sugar",
            "instructions": "Mix and bake.",
        }
        
        form = RecipeForm(data=form_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)
        self.assertIn("category", form.errors)

    def test_rating_form_valid(self):
        form_data = {"rating": 4}
        form = RatingForm(data=form_data)
        
        self.assertTrue(form.is_valid())

    def test_rating_form_invalid(self):
        form_data = {"rating": 6}  
        form = RatingForm(data=form_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn("rating", form.errors)
        
    

class SavedRecipeTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.category = Category.objects.create(name="Desserts")
        self.recipe = Recipe.objects.create(
            title="Chocolate Cake",
            author=self.user,
            category=self.category,
            description="Delicious chocolate cake",
            difficulty="Easy",
            ingredients="Flour, Sugar, Cocoa",
            instructions="Mix and bake",
        )
    
    def test_prevent_duplicate_saves(self):
        SavedRecipe.objects.create(user=self.user, recipe=self.recipe)
        
        with self.assertRaises(Exception):
            SavedRecipe.objects.create(user=self.user, recipe=self.recipe)



class CommentModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.category = Category.objects.create(name="Desserts")
        self.recipe = Recipe.objects.create(
            title="Chocolate Cake",
            author=self.user,
            category=self.category,
            description="Delicious chocolate cake",
            difficulty="Easy",
            ingredients="Flour, Sugar, Cocoa",
            instructions="Mix and bake",
        )
    
    def test_comment_creation(self):
        comment = Comment.objects.create(user=self.user, recipe=self.recipe, text="Looks tasty!")
        
        self.assertEqual(comment.text, "Looks tasty!")
        self.assertEqual(self.recipe.comments.count(), 1)




