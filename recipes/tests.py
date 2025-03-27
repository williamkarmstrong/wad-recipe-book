from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


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



