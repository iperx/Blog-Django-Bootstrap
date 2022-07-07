from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views import generic

from .forms import PostForm, TagForm, SignUpForm, SignInForm
from .models import Post, Tag
from .utils import (
    ObjectCreateMixin,
    ObjectUpdateMixin,
    ObjectDeleteMixin
)


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'blog/sign_up.html'
    success_url = reverse_lazy('sign_in_url')


class SignInView(LoginView):
    form_class = SignInForm
    template_name = 'blog/sign_in.html'

    def get_success_url(self):
        return reverse_lazy('posts_list_url')


class SignOutView(LogoutView):
    next_page = reverse_lazy('posts_list_url')


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.prefetch_related('tags')
    paginate_by = 3
    template_name = 'blog/index.html'


class PostDetails(generic.DetailView):
    model = Post
    queryset = Post.objects.all()
    template_name = 'blog/post_details.html'


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


class TagList(generic.ListView):
    model = Tag
    queryset = Tag.objects.all()
    template_name = 'blog/tags_list.html'
    paginate_by = 5


class TagDetails(generic.ListView):
    template_name = 'blog/tag_details.html'
    paginate_by = 3

    def get_queryset(self):
        tag = get_object_or_404(Tag, slug=self.kwargs.get('slug'))
        posts = Post.objects.prefetch_related('tags').filter(
            tags__slug=tag.slug
        )
        self.extra_context = {
            'tag': tag,
        }
        return posts

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