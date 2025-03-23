from django import forms
from comment.models.comment_models import Comment





class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ['name','email','subject','message']