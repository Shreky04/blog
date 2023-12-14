from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Post, Comments, User, Subscribe


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ("published_date", "comment", "user")

class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        exclude = ("published_date", "author", "post")


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscribe
        fields = ['email']

class UserProfileCreationForm(UserCreationForm):
    phone = forms.CharField(max_length=20, required=False)
    dateofbirth = forms.DateField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'phone', 'dateofbirth']

