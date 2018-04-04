from django import forms
from .models import Comment
from django.contrib.auth import get_user_model

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['name','email','url','text']
