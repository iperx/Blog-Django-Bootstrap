from time import time

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from .models import Post, Tag


class SlugMixin():
    """Adds methods to set unique slug based on title and Unix time"""

    def clean_slug(self):
        """Get unique value for hidden empty slug field"""

        data = self.cleaned_data['title']
        slug = self.generate_slug(data)
        return slug

    def generate_slug(self, title: str) -> str:
        """Generate unique slug using title and creation time"""

        new_slug = slugify(title, allow_unicode=True)
        if not new_slug:
            raise ValidationError(f"Title '{title}' is incorrect.")
        return f"{new_slug}-{time():.0f}"


class PostForm(SlugMixin ,forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'slug', 'body', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.HiddenInput(),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }


class TagForm(SlugMixin, forms.ModelForm):
    
    class Meta:
        model = Tag
        fields = ['title', 'slug']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.HiddenInput(),
        }


class SignUpForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given username
    and password.
    """

    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Confirm password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    
class SignInForm(AuthenticationForm):
    """A form that accepts username/password logins."""
    
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
