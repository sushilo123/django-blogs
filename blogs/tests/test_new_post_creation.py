import uuid

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from blogs.models import Post

User = get_user_model()

class NewBlogTestCase(TestCase):

    def setUp(self):
        self.posts = [
            Post(
                uuid=uuid.uuid4(),
                author='user@example.com',
                heading='post 1',
                content='post 1 content'
            ),
            Post(
                uuid=uuid.uuid4(),
                author='user@example.com',
                heading='post 2',
                content='post 2 content'
            )
        ]
        Post.objects.bulk_create(self.posts)
        self.author_user = User.objects.create_user(username='authoruser', password='authorpassword')
        self.author_user.author.is_author = True
        self.author_user.author.save()
        self.normal_user = User.objects.create_user(username='normaluser', password='noramlpassword')
        self.url = reverse('blogs:new')
    
    def test_new_post_creation_with_author_user(self):
        """
        Checks that a new post is created when a user with
        author status makes a request.
        """
        init_post_count = Post.objects.count()
        self.client.force_login(self.author_user)
        response = self.client.get(self.url)
        new_post_count = Post.objects.count()
        # check that only one new post has been created
        self.assertEqual(new_post_count, init_post_count + 1)
    
    def test_forbidden_for_non_author_user(self):
        """
        Tests that the response returned is 403 Forbidden if the
        user is not logged in.
        """
        self.client.force_login(self.normal_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)
    
    def test_new_post_redirect_to_editor(self):
        """
        Checks that after a new post is creatd user is redirected
        to the edit view of the post.
        """
        self.client.force_login(self.author_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        
