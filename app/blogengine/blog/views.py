from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View
from django.core.paginator import Paginator
from django.db.models import Q

from .models import *
from .utils import *
from .forms import *


def paginate(request, posts):
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    is_paginated = page.has_other_pages()

    if page.has_next():
        next_url = 'page={}'.format(page.next_page_number())
    else:
        next_url = ''
    if page.has_previous():
        prev_url = 'page={}'.format(page.previous_page_number())
    else:
        prev_url = ''

    context = {
        'page_obj': page,
        'next_url': next_url,
        'prev_url': prev_url,
        'is_paginated': is_paginated,
    }
    return context


def posts_list(request):
    search_query = request.GET.get('search', '')
    if search_query:
        posts = Post.objects.filter(
            Q(title__icontains=search_query) | Q(body__icontains=search_query)
            )
    else:
        posts = Post.objects.all()

    context = paginate(request, posts)
    context['search'] = search_query

    return render(request, 'blog/index.html', context)


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


def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tags_list.html', context={'tags': tags})


class TagDetails(ObjectDetailsMixin, View):
    model = Tag
    template = 'blog/tag_details.html'


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