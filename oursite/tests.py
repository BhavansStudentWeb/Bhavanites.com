from django.test import TestCase, SimpleTestCase
from django.contrib.auth.models import User

class UserLoginTests(TestCase):

    def test_user_not_logged_in(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,'/login/')

    def test_user_logged_in(self):
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'oursite/home.html')
