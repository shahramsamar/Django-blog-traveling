from django.shortcuts import render
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView,)
from blog.models.blog_models import Post,Category


class BlogHomeView(ListView):
    model = Post
    template_name = 'blog.html'
    context_object_name = 'posts'
    success_url = '/'
    paginate_by = 4
    
# def BlogView(request):
#     # template_name ='blog.html'
#     return render(request,'blog.html')

def SingleBlogView(request):
    return render(request,'single.html')