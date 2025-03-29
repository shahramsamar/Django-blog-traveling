from django import forms
from comment.models.comment_models import Comment





class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['parent','content']
        # widgets = {
        #     'parent': forms.HiddenInput(),
        #     'message': forms.Textarea(attrs={'rows': 2}),
        # }