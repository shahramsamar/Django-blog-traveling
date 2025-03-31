from django import forms
from blog.models.blog_models import NewsLetter


class NewsLetterForm(forms.ModelForm):

    class Meta:
        model = NewsLetter
        fields = "__all__"
