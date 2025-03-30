# from django import forms
# from comment.models.comment_models import Comment


# class CommentForm(forms.ModelForm):
#     parent = forms.IntegerField(widget=forms.HiddenInput(), required=False)

#     class Meta:
#         model = Comment
#         fields = ['content', 'parent']
#         widgets = {
#             'content': forms.Textarea(attrs={'rows': 3,   'cols':10 , 'class': 'form-control', 'placeholder': 'Write your comment here...'}),
#         }
from django import forms
from comment.models.comment_models import Comment

class CommentForm(forms.ModelForm):
    parent = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Comment
        fields = ['content', 'parent']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3, 
                'cols': 10, 
                'class': 'form-control', 
                'placeholder': 'Write your comment here...'
            }),
        }

    def clean_parent(self):
        parent = self.cleaned_data.get('parent')
        if parent:
            try:
                return Comment.objects.get(pk=parent)
            except Comment.DoesNotExist:
                raise forms.ValidationError("Invalid parent comment.")
        return None
