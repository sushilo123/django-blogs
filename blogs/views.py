import uuid

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpResponse

from .models import Post
from .mixins import AuthorRequiredMixin


class BlogHomeView(View):
    
    def get(self, request):
        posts_list = Post.objects.filter(is_deleted=False, is_published=True)
        paginator = Paginator(posts_list, 25)

        page = request.GET.get('page')
        posts = paginator.get_page(page)
        return render(request, 'django-blogs/home.html', {
            'posts': posts
        })

class NewBlogView(LoginRequiredMixin, AuthorRequiredMixin, View):

    def get(self, request):
        post = Post.objects.create(
            author=request.user.username,
            uuid=uuid.uuid4(),
            heading="Click to edit Title",
            content="Click to edit body"
        )
        return redirect('blog:edit', uuid=post.uuid)

class BlogEditView(LoginRequiredMixin, AuthorRequiredMixin, View):

    def get(self, request, uuid):
        post = get_object_or_404(Post, pk=uuid)
        return render(request, 'django-blogs/editor.html', {
            'blog': post
        })
    
    def post(self, request, uuid):
        pass