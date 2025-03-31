from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from blog.models.blog_models import Post, Category, TaggableManager
from django.db.models import Q, Count, F
from taggit.models import Tag
from blog.forms.newsletter import NewsLetterForm
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models.functions import TruncMonth
from django.views.generic.dates import MonthArchiveView
from comment.models.comment_models import Comment
from comment.forms.comment import CommentForm
from django.db.models import Prefetch
from django.contrib import messages
from accounts.models.users_models import User


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
        queryset = (
            super()
            .get_queryset()
            .filter(is_published=True)
            .annotate(
                comment_count=Count("comments", filter=Q(comments__approved=True))
            )
        )
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
        return HttpResponseRedirect("/")

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
        context["newsletter_form"] = NewsLetterForm()
        context["archives"] = (
            Post.objects.annotate(date=TruncMonth("created_date"))
            .values("date")
            .annotate(count=Count("id"))
            .order_by("date")
        )
        return context


class MonthlyArchiveView(MonthArchiveView):
    model = Post
    allow_future = False
    context_object_name = "posts"
    template_name = "sidebar/archive_view.html"
    month_format = "%m"
    date_field = "created_date"
    paginate_by = 5  # Optional pagination

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .filter(
                is_published=True,
                created_date__year=self.get_year(),
                created_date__month=self.get_month(),
            )
            .annotate(
                comment_count=Count("comments", filter=Q(comments__approved=True))
            )
        )
        return queryset


class SingleBlogView(DetailView):
    model = Post
    template_name = "single.html"
    context_object_name = "post"
    pk_url_kwarg = "pk"

    def get_queryset(self):
        """Returns published posts with comment count"""
        return (
            super()
            .get_queryset()
            .filter(is_published=True)
            .annotate(
                comment_count=Count("comments", filter=Q(comments__approved=True))
            )
        )

    def post(self, request, *args, **kwargs):
        """Handle comment form submission"""
        self.object = self.get_object()
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = self.request.user
            parent_id = request.POST.get("parent")
            if parent_id:
                try:
                    parent_comment = Comment.objects.get(id=parent_id)
                    comment.parent = parent_comment  # Correctly assign parent comment
                except Comment.DoesNotExist:
                    pass  # Ignore invalid parent comments

            comment.save()
            messages.success(request, "Your comment has been submitted for moderation!")
        else:
            messages.error(request, "Please correct the errors in the form.")

        return redirect(self.object.get_absolute_url() + "#comments")

    def get_context_data(self, **kwargs):
        """Add additional context"""
        context = super().get_context_data(**kwargs)
        if "pk" in self.kwargs:
            post = get_object_or_404(Post, pk=self.kwargs["pk"])
            post.views += 1  # Manually increment
            post.save(update_fields=["views"])  # Save changes
            # print(f"Updated views count: {post.views}")  # Debugging
            # print(self.request) # Show result

        context["search_term"] = self.request.GET.get("s", "")
        context["latest_post"] = self.get_queryset().order_by("-created_date")[:3]
        context["categories"] = (
            Post.objects.values("category__name")
            .annotate(post_count=Count("id"))
            .filter(post_count__gt=0)
            .order_by("category__name")
        )
        context["all_tags"] = Post.tags.all()
        context["newsletter_form"] = NewsLetterForm()
        context["archives"] = (
            Post.objects.annotate(date=TruncMonth("created_date"))
            .values("date")
            .annotate(count=Count("id"))
            .order_by("date")
        )
        context["comment_form"] = CommentForm()
        context["comments"] = self.object.comments.filter(
            approved=True
        ).prefetch_related(
            Prefetch("replies", queryset=Comment.objects.filter(approved=True))
        )
        return context


class PostCommentView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "single.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs["pk"])
        # The parent field is now already cleaned to be a Comment instance (or None)
        form.instance.parent = form.cleaned_data.get("parent")
        form.instance.save()
        messages.success(
            self.request, "Your comment has been submitted for moderation!"
        )
        return redirect(
            reverse("single", kwargs={"pk": self.kwargs["pk"]}) + "#comments"
        )

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors in the form.")
        return super().form_invalid(form)
