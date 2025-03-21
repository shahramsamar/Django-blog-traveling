from django.shortcuts import render
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView,)
from blog.models.blog_models import Post,Category
from django.db.models import Q,Count


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
        
        
        category = self.kwargs.get('category')
        if category:
            return queryset.filter(category__name__iexact=category)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        """ 
       set context with queryset  and  return 
        """
        context = super().get_context_data(**kwargs)
        context['search_term'] = self.request.GET.get('s','')
        context['latest_post'] = self.get_queryset().order_by('is_published')[:3]
        # context['categories'] = Category.objects.filter(post__in=self.get_queryset())
        context['categories'] = ( Post.objects.values('category__name').annotate(post_count=Count('id')).order_by('category__name').filter(post_count__gt=0) )

        # for cat in context['categories']:

        #     context['categories'][cat.name] = cat.post_count
        #     context['count'] += 1
        #         # context['cat_count'] = Category.objects.filter(category_count__gt=0).order_by('name')

        # print(context['categories'].values())
        # for k,v in context['categories']:
        #     print(k,v)
        # print(context.keys())
        # print(context['latest_post'])
        # print(context['paginator'])
        # print(context['page_obj'])
        # print(context['is_paginated'])
        # print(context['object_list'])
        # print(context['posts'])
        # print(context['view'])
        return context
    
    

def SingleBlogView(request):
    return render(request,'single.html')