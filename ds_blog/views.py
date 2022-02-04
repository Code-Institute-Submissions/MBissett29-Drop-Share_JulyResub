from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, View, CreateView
from .models import Post
from .forms import UserPostForm, CommentForm
from django.http import HttpResponseRedirect
from django.utils.text import slugify

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
        form = UserPostForm()
        context = {'form': form}
        return render(request, "post_blog.html", context=context)

    def form_valid(self, form):
        """This saves the blog entry and saves and returns the user"""
        print(self.request.user)
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)
