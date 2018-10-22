from django.test import TestCase
from django.urls import reverse

from blogs.models import Post

class HomeViewTestCase(TestCase):
    
    def setUp(self):
        self.url = reverse("blogs:home")

    def test_blog_home_uses_home_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'django-blogs/home.html')
        