from django import forms
from .models import Post,Comment # imported Post and Comment Models


class PostForm(forms.ModelForm):

    body  =forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows':'3',
            'placeholder':'What are you upto ?'
        })
    ) # only text body taken as input
    
    class Meta:
        model = Post # connected to Post Model
        fields = ['body'] # left it as textbody currently, will update to Pictures and Captions later 


class CommentForm(forms.ModelForm):

    comment  =forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows':'3',
            'placeholder':' Add comment'
        })
    ) # only text body taken as input
    
    class Meta:
        model = Comment # connected to Comment Model
        fields = ['comment']