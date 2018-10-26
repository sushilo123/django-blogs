import uuid

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from blogs.models import Post

User = get_user_model()

class PostEditorTestCase(TestCase):

    def setUp(self):
        self.author1 = User.objects.create_user(username='author1', password='authorpassword')
        self.author2 = User.objects.create_user(username='author2', password='authorpassword')
        self.normal_user = User.objects.create_user(username='normal_user', password='normalpassword')
        self.author1.author.is_author = True
        self.author2.author.is_author = True
        self.post1 = Post.objects.create(
            uuid=uuid.uuid4(),
            author=self.author1.username,
            heading="Post 1",
            content="<p>Post 1 content</p>"
        )
        self.post2 = Post.objects.create(
            uuid=uuid.uuid4(),
            author=self.author2.username,
            heading="Post 2",
            content="<p>Post 2 content</p>"
        )
        self.url1 = reverse('blogs:edit', kwargs={'uuid': self.post1.uuid})
        self.url2 = reverse('blogs:edit', kwargs={'uuid': self.post2.uuid})
    
    def test_get_editor_template_render(self):
        """
        Tests if the template used to render is editor.html
        """
        self.client.force_login(self.author1)
        response = self.client.get(self.url1)
        self.assertTemplateUsed(response, 'django-blogs/editor.html')
    
    def test_get_editor_forbidden_for_other_author(self):
        """
        Tests that the original author is only allowed to edit
        """
        self.client.force_login(self.author2)
        response = self.client.get(self.url1)
        self.assertEqual(response.status_code, 403)
    
    def test_get_editor_redirect_for_no_auth(self):
        """
        Tests that authentication is required for editor.
        """
        self.client.logout()
        response = self.client.get(self.url1)
        self.assertEqual(response.status_code, 302)
    
    def test_editor_forbidden_for_non_author(self):
        """
        Tests that editor is forbidden for non author user.
        """
        self.client.force_login(self.normal_user)
        response = self.client.get(self.url2)
        self.assertEqual(response.status_code, 403)
        response = self.client.post(self.url2)
        self.assertEqual(response.status_code, 403)
    
    def test_save_bad_request(self):
        """
        Tests 400 response on bad request.
        """
        self.client.force_login(self.author1)
        response = self.client.post(self.url1)
        self.assertEqual(response.status_code, 400)
        # when only heading is provided
        response = self.client.post(self.url1, data={'heading': 'New heading'})
        self.assertEqual(response.status_code, 400)
        # when only content is provided
        response = self.client.post(self.url1, data={'content': 'New content'})
        self.assertEqual(response.status_code, 400)
    
    def test_save_ok(self):
        """
        Tests 200 response if the request is good.
        """
        self.client.force_login(self.author2)
        response = self.client.post(
            self.url2,
            data={
                'heading': 'New heading',
                'content': 'New Content',
        })
        self.assertEqual(response.status_code, 200)
    
    def test_save_forbidden_on_other_author(self):
        """
        Tests that post request returns 402 forbidden
        when the logged in user in not the author of the 
        post.
        """
        self.client.force_login(self.author1)
        response = self.client.post(
            self.url2,
            data={
                'heading': 'New heading',
                'content': 'New Content',
        })
        self.assertEqual(response.status_code, 403)