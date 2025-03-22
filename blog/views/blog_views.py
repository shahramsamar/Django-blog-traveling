from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from blog.models.blog_models import Post, Category, TaggableManager
from django.db.models import Q, Count
from taggit.models import Tag
from blog.forms.form import NewsLetterForm
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect


class BlogHomeView(ListView):
    """ """

    model = Post
    template_name = "blog.html"
    context_object_name = "posts"
    success_url = "/"
    paginate_by = 4
    ordering = ["-created_date"]

    def get_queryset(self):
        """
        get search item in title and content
        """
        queryset = super().get_queryset().filter(is_published=True)

        search_term = self.request.GET.get("s")
        # print(search_term)
        if search_term:
            return queryset.filter(
                Q(title__icontains=search_term) | Q(content__icontains=search_term)
            )
        # print(queryset)

        category = self.kwargs.get("category")
        # print(category)
        if category:
            return queryset.filter(category__name__iexact=category)
        # print(queryset)

        tag_name = self.kwargs.get("tag")
        # print(tag_name)
        if tag_name:
            return queryset.filter(tags__name__iexact=tag_name)
        # print(queryset)

        return queryset


    def post(self, request, *args, **kwargs):
        """
            Handle newsletter subscription form submission
        """
        form = NewsLetterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for subscribing to our newsletter!")
        else:
            messages.error(request, "Invalid email address. Please try again.")
            
        return HttpResponseRedirect('/')
        


    def get_context_data(self, **kwargs):
        """
        set context with queryset  and  return
        """
        context = super().get_context_data(**kwargs)
        context["search_term"] = self.request.GET.get("s", "")
        context["latest_post"] = self.get_queryset().order_by("-created_date")[:3]
        context["categories"] = (
            Post.objects.values("category__name")
            .annotate(post_count=Count("id"))
            .order_by("category__name")
            .filter(post_count__gt=0)
        )
        context["all_tags"] = Post.tags.all()
        context['newsletter_form'] = NewsLetterForm()

        return context


        
class SingleBlogView(BlogHomeView):
    model = Post
    template_name = "single.html"
    context_object_name = "posts"

    # def get_queryset(self):
    #     """
    #     get search item in title and content
    #     """
    #     queryset = super().get_queryset()

    #     search_term = self.request.GET.get("s")
    #     if search_term:
    #         return queryset.filter(Q(title__icontains=search_term) | Q(content__icontains=search_term))

    #     category = self.kwargs.get('category')
    #     if category:
    #         return queryset.filter(category__name__iexact=category)

    #     return queryset

    # def get_context_data(self, **kwargs):
    #     """
    #    set context with queryset  and  return
    #     """
    #     context = super().get_context_data(**kwargs)
    #     context['search_term'] = self.request.GET.get('s','')
    #     context['latest_post'] = self.get_queryset().order_by('is_published')[:3]
    #     context['categories'] = (Post.objects.values('category__name').annotate(post_count=Count('id')).order_by('category__name').filter(post_count__gt=0) )
    #     return context
