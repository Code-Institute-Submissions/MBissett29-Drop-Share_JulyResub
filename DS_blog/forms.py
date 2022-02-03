from django import forms
from .models import Comment, UserPost


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


class UserPostForm(forms.ModelForm):
    class Meta:
        model = UserPost
        fields = ('title', "content",)