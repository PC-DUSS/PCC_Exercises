from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .models import BlogPost
from .forms import BlogPostForm

# Create your views here.


def index(request):
    """Display home page. If user logged in, display 3 most recent blog
    posts."""
    blog_posts = BlogPost.objects.order_by("-date_added")[:3]
    context = {'blog_posts': blog_posts}
    return render(request, "blogs/index.html", context)


def blog_posts(request):
    """Display all blog posts, in order of last added first."""
    blog_posts = BlogPost.objects.order_by("date_added")
    context = {'blog_posts': blog_posts}
    return render(request, "blogs/blog_posts.html", context)


def post(request, post_id):
    """Display a single blog post in its entirety."""
    post = BlogPost.objects.get(id=post_id)
    return render(request, "blogs/post.html", {'post': post})


@login_required
def new_blog_post(request):
    """Page to create a new blog post."""
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = BlogPostForm(request.POST)
            if form.is_valid():
                new_blog_post = form.save(commit=False)
                new_blog_post.owner = request.user
                new_blog_post.save()
                return redirect("blogs:blog_posts")
        else:
            form = BlogPostForm()

        return render(request, "blogs/new_blog_post.html", {'form': form})
    else:
        raise Http404


@login_required
def edit_blog_post(request, post_id):
    """Page to edit an existing blog post."""
    blog_post = BlogPost.objects.get(id=post_id)
    check_owner(blog_post.owner, request.user)
    if request.method == 'POST':
        form = BlogPostForm(data=request.POST, instance=blog_post)
        if form.is_valid():
            form.save()
            return redirect("blogs:blog_posts")
    else:
        form = BlogPostForm(instance=blog_post)

    return render(request, "blogs/edit_blog_post.html",
                  {'form': form, 'post_id': post_id})


def check_owner(owner, current_user):
    """Checks if current user is the owner of the item he wishes to see or
    modify."""
    if owner != current_user:
        raise Http404
