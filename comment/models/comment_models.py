from django.db import models
from  blog.models.blog_models import Post
from django.urls import reverse
from django.contrib.auth.models import User





class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    image = models.ImageField(upload_to='profile/user',default='profile/profile.jpeg')
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    approved = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    
    # def __str__(self):
        # return self.name
    
    class Meta:
        ordering = ['created_date']
    
    # def get_absolute_url(self):
    #     return reverse("single", kwargs={"pk": self.pk})
        
    def __str__(self):
        return f"Comment by {self.get_author_name()} on {self.post}"

    def get_author_name(self):
        return self.author.username if self.author else self.name