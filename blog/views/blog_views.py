from django.shortcuts import render
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView,)
from blog.models.blog_models import Post,Category
from django.db.models import Q

class BlogHomeView(ListView):
    """
    """
    model = Post
    template_name = 'blog.html'
    context_object_name = 'posts'
    success_url = '/'
    paginate_by = 4
    ordering = ['-created_date']
    
    
    def get_queryset(self):
        """ 
        get search item in title and content
        """
        queryset = super().get_queryset()
        # print(queryset)
        search_term = self.request.GET.get("s")
        if search_term:
            return queryset.filter(Q(title__icontains=search_term) | Q(content__icontains=search_term))
        return queryset
    
    def get_context_data(self, **kwargs):
        """ 
       set context with queryset  and  return 
        """
        context = super().get_context_data(**kwargs)
        context['search_term'] = self.request.GET.get('s','')
        context['latest_post'] = self.get_queryset().order_by('is_published')[:3]
        # print(context.keys())
        # print(context['latest_post'])
        return context
    
    

def SingleBlogView(request):
    return render(request,'single.html')