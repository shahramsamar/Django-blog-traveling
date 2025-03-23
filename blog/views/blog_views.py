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
from blog.forms.newsletter import NewsLetterForm
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models.functions import TruncMonth
from django.views.generic.dates import MonthArchiveView
from comment.models.comment_models import Comment
from comment.forms.comment import CommentForm
from django.shortcuts import redirect


class BlogHomeView(ListView):
    """ 
    
    """
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
        if search_term:
            return queryset.filter(
                Q(title__icontains=search_term) | Q(content__icontains=search_term)
            )

        category = self.kwargs.get("category")
        if category:
            return queryset.filter(category__name__iexact=category)

        tag_name = self.kwargs.get("tag")
        if tag_name:
            return queryset.filter(tags__name__iexact=tag_name)

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
        context['archives'] = Post.objects.annotate(date=TruncMonth('created_date')).values('date').annotate(count=Count('id')).order_by('date')
        return context


class MonthlyArchiveView(MonthArchiveView):
    model = Post
    allow_future = False
    context_object_name = 'posts'
    template_name = 'post_archive_view.html'
    month_format = '%m'
    date_field = 'created_date'
    paginate_by = 5 # Optional pagination
    
    def get_queryset(self):
        return super().get_queryset().filter(created_date__year=self.get_year(), created_date__month=self.get_month())
    



        
class SingleBlogView(DetailView):
    model = Post
    template_name = "single.html"
    context_object_name = "post"
    pk_url_kwarg = 'pk'
    # allow_future = True

    # def post(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     # print(object)
    #     form = CommentForm(request.POST)
        
    #     if form.is_valid():
    #         comment = form.save(commit=False)
    #         # print(comment)
    #         comment.post = self.object
    #         # print(comment)
    #         comment.save()
    #         messages.success(request, "Your comment is awaiting moderation!")
    #         return redirect(self.object.get_absolute_url())  # Changed from HttpResponseRedirect
        
    #     messages.error(request, "Please correct the errors below.")
    #     return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        """Handle comment form submission"""
        self.object = self.get_object()
        form = CommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object  # Link comment to post
            comment.save()
            messages.success(request, "Your comment has been submitted for moderation!")
        else:
            messages.error(request, "Please correct the errors in the form.")
        
        return redirect(self.object.get_absolute_url())

    def get_context_data(self, **kwargs):
        """
        set context with  return data
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
        context['archives'] = Post.objects.annotate(date=TruncMonth('created_date')).values('date').annotate(count=Count('id')).order_by('date')
        # context['comments'] = self.object.comments.filter(approved=True)
        # print(context['comments'])
        context['comment_form'] = CommentForm()
        # print(context['comment_form'])
        return context
# context['archives'] = Post.objects.annotate(date=TruncMonth('created_date')).values('date').annotate(count=Count('id')).order_by('date')