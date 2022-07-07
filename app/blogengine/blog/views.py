from django.contrib.auth.mixins import LoginRequiredMixin
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['admin_object'] = self.object
        return context


class PostCreate(LoginRequiredMixin, generic.CreateView):
    form_class = PostForm
    template_name = 'blog/post_create.html'


class PostUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_update.html'


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
    """Retrieves all posts containing a particular tag"""
    
    model = Tag
    template_name = 'blog/tag_details.html'
    paginate_by = 3

    def get(self, request, *args, **kwargs):
        # The variable is made to avoid multiple similar queries
        # and to have the tag object always on hand
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def get_object(self):
        return get_object_or_404(self.model, slug=self.kwargs.get('slug'))

    def get_queryset(self):
        posts = Post.objects.prefetch_related('tags').filter(
            tags__slug=self.object.slug
        )
        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'tag': self.object,
            'admin_object': self.object,
        })
        return context


class TagCreate(LoginRequiredMixin, generic.CreateView):
    form_class = TagForm
    template_name = 'blog/tag_create.html'


class TagUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Tag
    form_class = TagForm
    template_name = 'blog/tag_update.html'


class TagDelete(ObjectDeleteMixin, View):
    model = Tag
    template = 'blog/tag_delete.html'
    redirect_url = 'tags_list_url'