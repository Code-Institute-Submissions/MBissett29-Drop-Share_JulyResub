from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import ListView, View, CreateView
from django.http import HttpResponseRedirect
from .models import Post, Comment
from .forms import UserPostForm, CommentForm
from django.utils.text import slugify
from django.contrib import messages

class PostList(ListView):
    """This creates a list of blog entrys to the main page"""
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 8


class PostDetail(View):
    """This create a detailed view of the blog post in detail"""

    def get(self, request, slug, *args, **kwargs):
        """This gets the combines the comments and blog post and likes together"""
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('-created_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "user_post.html",
            {
                "post": post,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )

    def post(self, request, slug, *args, **kwargs):
        """This gets the combines the comments and blog post and likes together"""
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('-created_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            "user_post.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )


class UserPost_Create(CreateView):
    """This creates the the view for blog post entry page"""
    model = Post
    template_name = 'post_blog.html'
    fields = ('title', 'content', 'featured_image')

    def get(self, request, *args, **kwargs):
        """This grabs the form of the blog entry"""
        UserPost_form = UserPostForm()
        context = {'UserPost_form': UserPostForm}
        return render(request, "post_blog.html", context=context, )

    def form_valid(self, form):
        """This saves the blog entry and saves and returns the user"""
        print(self.request.user)
        if form.is_valid:
            form.instance.author = self.request.user
            form.instance.slug = slugify(form.instance.title)
            messages.success(self.request, "Your post is pending approval")
            return super().form_valid(form)
        messages.error(self.request, "Error occured please try again")
        UserPost_form = UserPostForm()
        context = {'UserPost_form': UserPostForm}
        return render(request, "post_blog.html", context=context, )

        

class PostLike(View):
    
    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('user_post', args=[slug]))