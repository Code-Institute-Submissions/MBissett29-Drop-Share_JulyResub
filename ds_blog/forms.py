from django import forms
from .models import Comment, Post


class CommentForm(forms.ModelForm):
    """This creates a comment box for user to leave comment"""
    class Meta:
        """This selects the model of Comment and uses specifc fields"""
        model = Comment
        fields = ('body',)


class UserPostForm(forms.ModelForm):
    """This creates the User to upload their own blog"""
    class Meta:
        """This selects the model of post and uses specifc fields"""
        model = Post
        fields = ('title', "content", "featured_image",)

