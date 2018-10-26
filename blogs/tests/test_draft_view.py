import uuid

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class DraftViewTestCase(TestCase):
    
    def setUp(self):
        self.author_user = User.objects.create_user(username='author', password='authorpass')
        self.author_user.author.is_author = True
        self.author_user.save()
        self.normal_user = User.objects.create_user(username='normal', password='normalpass')
        self.url = reverse("blogs:drafts")

    def test_uses_drafts_template(self):
        self.client.force_login(self.author_user)
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'django-blogs/drafts.html')
    
    def test_auth_required(self):
        """
        Tests that authentication is required for this view.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
    
    def test_author_required(self):
        """
        Tests that normal user can not view drafts.
        """
        self.client.force_login(self.normal_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)
        