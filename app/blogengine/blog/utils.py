from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import *
from .forms import *


class ObjectDetailsMixin():
    model = None
    template = None

    def get(self, request, slug):
        obj = get_object_or_404(self.model, slug__iexact=slug)
        return render(request, self.template, context={
            self.model.__name__.lower(): obj,
            'admin_object': obj,
            })


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