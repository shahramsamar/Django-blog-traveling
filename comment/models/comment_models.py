from django.db import models
from  blog.models.blog_models import Post
from django.urls import reverse
from django.contrib.auth.models import User





class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, 
                                   on_delete=models.CASCADE, related_name='replies')
    content = models.TextField()
    approved = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_date']
  
    def __str__(self):
        return f"Comment by {self.get_author_name()} on {self.post}"

    def get_author_name(self):
        return self.author or self.author 


# class Replay(models.Model):
#     author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,related_name='replies')
#     parent_comment = models.ForeignKey(Comment , null=True , blank=True , on_delete=models.CASCADE , related_name='child_replies')
#     name = models.CharField(max_length=50)
#     message = models.TextField()
#     approved = models.BooleanField(default=False)
#     created_date = models.DateTimeField(auto_now_add=True)
#     updated_date = models.DateField(auto_now=True)
    
#     class Meta:
#         ordering = ['created_date']
  
#     def __str__(self):
#         return f"Reply by {self.get_author_name()} to {self.parent_comment}"

#     def get_author_name(self):
#         return self.author.username if self.author else self.name    