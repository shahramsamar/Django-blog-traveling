from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.urls import reverse


class Category(models.Model):
    """ """

    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name


class Post(models.Model):
    """ """

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="imgage/post", default="default/")
    category = models.ManyToManyField(Category, blank=True)
    tags = TaggableManager(blank=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    is_published = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_snipper(self):
        return self.content[0:150]

    # def get_absolute_url(self):
    #     return reverse("single", kwargs={"pk": self.pk})
    # def get_absolute_url(self):
    #     return reverse('blog', args=[str(self.id)])

class NewsLetter(models.Model):
    email = models.EmailField()
    
    
    def __str__(self):
        return self.email