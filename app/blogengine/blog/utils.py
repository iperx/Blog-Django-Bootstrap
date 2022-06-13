from collections import namedtuple

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404


class PaginationMixin:
    """Adds pagination"""

    pagination = False
    page_size = 3

    def paginate(self, obj_list, page_number):
        """
        Paginate a QuerySet object. Returns context dictionary with keys:
        page_obj, next_url, prev_url, is_paginated
        """
        paginator = Paginator(obj_list, self.page_size)
        page = paginator.get_page(page_number)
        is_paginated = page.has_other_pages()

        next_url = prev_url = ''
        if page.has_next():
            next_url = 'page={}'.format(page.next_page_number())
        if page.has_previous():
            prev_url = 'page={}'.format(page.previous_page_number())

        context = {
            'page_obj': page,
            'next_url': next_url,
            'prev_url': prev_url,
            'is_paginated': is_paginated,
        }
        return context


class SearchMixin:
    """Adds a simple search for model objects"""

    def search(self, search_query):
        """
        Look up for particular results according to user search query.
        Returns QuerySet object
        """
        if hasattr(self.model, 'body'):
            obj_list = self.model.objects.filter(
                Q(title__icontains=search_query) |
                Q(body__icontains=search_query)
            )
        else:
            obj_list = self.model.objects.filter(
                title__icontains=search_query
                )
        return obj_list


class ObjectListMixin(PaginationMixin, SearchMixin):
    model = None
    template = None

    def get(self, request):
        """
        Returns rendered page with list of objects depending on search results and pagination
        """
        search_query = request.GET.get('search')
        if search_query:
            obj_list = self.search(search_query)
        else:
            obj_list = self.model.objects.all()

        if self.pagination:
            page_number = request.GET.get('page', 1)
            context = self.paginate(obj_list, page_number)
            context['search'] = search_query
        else:
            # namedtuple imitates class django.core.paginator.Page with
            # 'object_list' field. This is done to maintain common behaviour
            # across templates, whether the object list is paginated or not.
            obj_list = namedtuple('PageObjectStub', ['object_list'])(obj_list)
            context = {
                'page_obj': obj_list,
                'is_paginated': False
            }
        return render(request, self.template, context)


class ObjectDetailsMixin(PaginationMixin):
    model = None
    template = None

    def get(self, request, slug):
        obj = get_object_or_404(self.model, slug__iexact=slug)
        model_name = self.model.__name__
        context = {model_name.lower(): obj, 'admin_object': obj}
        if model_name != 'Tag':
            return render(request, self.template, context)

        obj_list = obj.posts.all()
        if self.pagination:
            page_number = request.GET.get('page', 1)
            context.update(self.paginate(obj_list, page_number))
        else:
            obj_list = namedtuple('PageObjectStub', ['object_list'])(obj_list)
            context.update({'page_obj': obj_list, 'is_paginated': False})
        return render(request, self.template, context)


class ObjectCreateMixin(LoginRequiredMixin):
    template = None
    model_form = None
    raise_exception = True

    def get(self, request):
        form = self.model_form
        return render(request, self.template, context={
            'form': form,
            'model': form._meta.model.__name__.lower(),
            })

    def post(self, request):
        bound_form = self.model_form(request.POST)
        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        else:
            return render(request, self.template, context={
                'form': bound_form,
                'model': bound_form._meta.model.__name__.lower(),
                })


class ObjectUpdateMixin(LoginRequiredMixin):
    model = None
    model_form = None
    template = None
    raise_exception = True

    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.model_form(instance=obj)
        return render(request, self.template, context={
            'form': bound_form, 
            'obj': obj,
            'model': self.model.__name__.lower(),
            })

    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.model_form(request.POST, instance=obj)
        if bound_form.is_valid():
            changed_obj = bound_form.save()
            return redirect(changed_obj)
        else:
            return render(request, self.template, context={
                'form': bound_form, 
                'obj': obj,
                'model': self.model.__name__.lower(),
                })


class ObjectDeleteMixin(LoginRequiredMixin):
    model = None
    template = None
    redirect_url = None
    raise_exception = True

    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        return render(request, self.template, context={
            self.model.__name__.lower(): obj
            })

    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        obj.delete()
        return redirect(self.redirect_url)