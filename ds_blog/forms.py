from django import forms
from .models import Comment, UserPost, Post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


class UserPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', "content", "featured_image")