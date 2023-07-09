from django import forms
from .models import Post,Comment # imported Post and Comment Models


class PostForm(forms.ModelForm):

    body  =forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows':'3',
            'placeholder':'What are you upto ?'
        })
    ) 

    image = forms.ImageField(required=False) # added image field
    
    class Meta:
        model = Post # connected to Post Model
        fields = ['body','image'] # added image field also


class CommentForm(forms.ModelForm):

    comment  =forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows':'3',
            'placeholder':' Add comment'
        })
    ) 
    
    class Meta:
        model = Comment 
        fields = ['comment']