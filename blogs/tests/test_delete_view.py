import uuid

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from blogs.models import Post

User = get_user_model()

class DeleteViewTestCase(TestCase):

    def setUp(self):
        self.author_user = User.objects.create_user(username='author', password='authorpass')
        self.author_user.author.is_author = True
        self.author_user.save()
        self.normal_user = User.objects.create_user(username='normal', password='normalpass')
        self.post1 = Post.objects.create(
            uuid=uuid.uuid4(),
            author=self.author_user.username,
            heading='Post Heading',
            content="<p>Post Content</p>",
        )
        self.post2 = Post.objects.create(
            uuid=uuid.uuid4(),
            author="other_author",
            heading='Post heading',
            content='Post Content',
        )
        self.url1 = reverse('blogs:delete', kwargs={'uuid': self.post1.uuid})
        self.url2 = reverse('blogs:delete', kwargs={'uuid': self.post2.uuid})
    
    def test_auth_required(self):
        """
        Tests that authentication is required for this view.
        """
        response = self.client.get(self.url1)
        self.assertEqual(response.status_code, 302)
    
    def test_author_required(self):
        """
        Tests that normal user can not delete.
        """
        self.client.force_login(self.normal_user)
        response = self.client.get(self.url1)
        self.assertEqual(response.status_code, 403)
    
    def test_same_author_required(self):
        """
        Tests that other author cannot delete.
        """
        self.client.force_login(self.author_user)
        response = self.client.get(self.url2)
        self.assertEqual(response.status_code, 403)
    
    def test_delete_same_author(self):
        """
        Tests that the post is deleted when author is correct.
        """
        self.assertFalse(self.post1.is_deleted)
        self.client.force_login(self.author_user)
        response = self.client.get(self.url1)
        self.assertEqual(response.status_code, 302)
        post = Post.objects.get(pk=self.post1.uuid)
        self.assertTrue(post.is_deleted)
    
    def test_404_on_invalid_uuid(self):
        """
        Tests that 404 not found is returned when the 
        post does not exist.
        """
        self.client.force_login(self.author_user)
        response = self.client.get(reverse('blogs:delete', kwargs={'uuid': 'abcdefab-abcd-1234-abcd-1234abcdef56'}))
        self.assertEqual(response.status_code, 404)