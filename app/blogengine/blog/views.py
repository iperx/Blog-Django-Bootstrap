from django.shortcuts import render

# Create your views here.
def posts_list(request):
    posts = ['One', 'Two', 'Three', 'Four', 'Five']
    return render(request, 'blog/index.html', context={'posts': posts})