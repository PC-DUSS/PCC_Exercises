from django.urls import path
from . import views

app_name = "blogs"
urlpatterns = [
    path("", views.index, name="index"),
    path("blog_posts/", views.blog_posts, name="blog_posts"),
    path("blog_posts/<int:post_id>/", views.post, name="post"),
    path("new_blog_post/", views.new_blog_post, name="new_blog_post"),
    path("edit_blog_post/<int:post_id>", views.edit_blog_post,
         name="edit_blog_post"),
]
