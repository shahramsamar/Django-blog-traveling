from django.db import models
from django.contrib.auth.models import User



class Category(models.Model):
    """
    """
    name = models.CharField(max_length=60)
    
    def __str__(self):
        return self.name
    


class Post(models.Model):
    """
    """
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='imgage/post',default='default/')
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,
                                 null=True,blank=True)
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
    #     return reverse("model_detail", kwargs={"pk": self.pk})
    
    
    