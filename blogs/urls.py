from django.urls import path

from . import views

app_name = 'blogs'

urlpatterns = [
    path('', views.BlogHomeView.as_view(), name="home"),
    path('new/', views.NewBlogView.as_view(), name="new"),
    path('<uuid:uuid>/edit', views.BlogEditView.as_view(), name="edit"),
]