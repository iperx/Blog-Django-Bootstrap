from django.urls import reverse_lazy
from django.views import View
from django.views import generic

from .forms import PostForm, TagForm, SignUpForm
from .models import Post, Tag
from .utils import (
    ObjectListMixin,
    ObjectDetailsMixin,
    ObjectCreateMixin,
    ObjectUpdateMixin,
    ObjectDeleteMixin
)


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'blog/sign_up.html'
    success_url = reverse_lazy('posts_list_url')


class PostList(ObjectListMixin, View):
    model = Post
    template = 'blog/index.html'
    pagination = True
    page_size = 3


class PostDetails(ObjectDetailsMixin, View):
    model = Post
    template = 'blog/post_details.html'


class PostCreate(ObjectCreateMixin, View):
    model_form = PostForm
    template = 'blog/post_create.html'


class PostUpdate(ObjectUpdateMixin, View):
    model = Post
    model_form = PostForm
    template = 'blog/post_update.html'


class PostDelete(ObjectDeleteMixin, View):
    model = Post
    template = 'blog/post_delete.html'
    redirect_url = 'posts_list_url'


class TagList(ObjectListMixin, View):
    model = Tag
    template = 'blog/tags_list.html'
    pagination = True
    page_size = 5


class TagDetails(ObjectDetailsMixin, View):
    model = Tag
    template = 'blog/tag_details.html'
    pagination = True
    page_size = 3


class TagCreate(ObjectCreateMixin, View):
    model_form = TagForm
    template = 'blog/tag_create.html'


class TagUpdate(ObjectUpdateMixin, View):
    model = Tag
    model_form = TagForm
    template = 'blog/tag_update.html'


class TagDelete(ObjectDeleteMixin, View):
    model = Tag
    template = 'blog/tag_delete.html'
    redirect_url = 'tags_list_url'