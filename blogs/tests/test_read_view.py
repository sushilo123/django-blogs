import uuid

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from blogs.models import Post

User = get_user_model()

class ReadViewTestCase(TestCase):

    def setUp(self):
        self.post1 = Post.objects.create(
            uuid=uuid.uuid4(),
            author='authoruser',
            heading='Post1 Heading',
            content='Post1 Content',
            slug='post1-heading-abcd',
            is_published=True,
        )
        self.post2 = Post.objects.create(
            uuid=uuid.uuid4(),
            author='authoruser',
            heading='Post2 Heading',
            content='Post2 Content',
            slug='post2-heading-abcd',
            is_published=False,
        )
        self.url1 = reverse("blogs:read", kwargs={'slug': self.post1.slug})
        self.url2 = reverse("blogs:read", kwargs={'slug': self.post2.slug})


    def test_read_uses_blog_template(self):
        """
        Tests that the template used is blog.html
        """
        response = self.client.get(self.url1)
        self.assertTemplateUsed(response, 'django-blogs/blog.html')
    
    def test_404_on_unpublished(self):
        """
        Tests 404 when the blog is unpublished.
        """
        response = self.client.get(self.url2)
        self.assertEqual(response.status_code, 404)
    
    def test_404_on_bad_slug(self):
        """
        Tests for not found on bad slug in url.
        """
        response = self.client.get(reverse(
            'blogs:read',
            kwargs={'slug': 'bad-bad-slug-not-found'}))
        self.assertEqual(response.status_code, 404)
