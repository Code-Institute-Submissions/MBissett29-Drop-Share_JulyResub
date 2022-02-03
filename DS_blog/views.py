from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, View
from .models import Post, UserPost
from .forms import UserPostForm, CommentForm
from django.http import HttpResponseRedirect

class PostList(ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 8


class PostDetail(View):

    def get(self, request, slug, *args, **kwargs):
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



def UserPost_Create(request):
    if request.method == 'POST':
        title = request.POST.get('blog_title')
        content = request.POST.get('blog_content')
        file = request.POST.get('add_image_file')
        UserPost.objects.create(title=title, content=content)

        return redirect('home')
    return render(request, "post_blog.html",)
