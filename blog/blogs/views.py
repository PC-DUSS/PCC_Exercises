from django.shortcuts import render, redirect
from .models import BlogPost
from .forms import BlogPostForm

# Create your views here.


def index(request):
    """Display home page."""
    return render(request, "blogs/index.html")


def most_recent(request):
    """Display the 3 most recent blog posts in more detail, in order of last
    added first."""
    blog_posts = BlogPost.objects.order_by("-date_added")[:3]
    return render(request, "blogs/most_recent.html",
                  {'blog_posts': blog_posts})


def blog_posts(request):
    """Display all blog posts, in order of last added first."""
    blog_posts = BlogPost.objects.order_by("date_added")
    return render(request, "blogs/blog_posts.html", {'blog_posts': blog_posts})


def post(request, post_id):
    """Display a single blog post in its entirety."""
    post = BlogPost.objects.get(id=post_id)
    return render(request, "blogs/post.html", {'post': post})


def new_blog_post(request):
    """Page to create a new blog post."""
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("blogs:blog_posts")
    else:
        form = BlogPostForm()

    return render(request, "blogs/new_blog_post.html", {'form': form})


def edit_blog_post(request, post_id):
    """Page to edit an existing blog post."""
    blog_post = BlogPost.objects.get(id=post_id)
    if request.method == 'POST':
        form = BlogPostForm(data=request.POST, instance=blog_post)
        if form.is_valid():
            form.save()
            return redirect("blogs:blog_posts")
    else:
        form = BlogPostForm(instance=blog_post)

    return render(request, "blogs/edit_blog_post.html",
                  {'form': form, 'post_id': post_id})
