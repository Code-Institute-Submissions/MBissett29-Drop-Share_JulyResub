from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


STATUS = ((0, "Draft"), (1, "Published"))


class Post(models.Model):
    """This creates a class base model for a blog post"""

    title = models.CharField(max_length=180, unique=True)
    slug = models.SlugField(max_length=180, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ds_blog_posts") # Need to think of name
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    featured_image = CloudinaryField('image', default='placeholder')
    excerpt = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(User, related_name='ds_blog_likes', blank=True)
    class Meta:
        """This orders the posts in ascending order"""
        ordering = ['created_on']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Returns user back to home page after submitting a post"""
        return reverse('home')

    def number_of_likes(self):
        """Reflects the number of likes on the specific post"""
        return self.likes.count()

    

class Comment(models.Model):
    """Creates a class base model for the comments"""
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=50)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    
    class Meta:
        """This orders the comments in descending order"""
        ordering = ['-created_on']

    def __str__(self):
        """This returns the comment body and the users name"""
        return f"Comment {self.body} by {self.name}"

