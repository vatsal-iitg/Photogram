from django import forms
from .models import Post,Comment # imported Post and Comment Models


class PostForm(forms.ModelForm):

    body  =forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows':'3',
            'placeholder':'What are you upto ?'
        })
<<<<<<< HEAD
    ) 

    image = forms.ImageField(required=False) # added image field
    
    class Meta:
        model = Post # connected to Post Model
        fields = ['body','image'] # added image field also
=======
    ) # only text body taken as input
    
    class Meta:
        model = Post # connected to Post Model
        fields = ['body'] # left it as textbody currently, will update to Pictures and Captions later 
>>>>>>> 2cf088b9dfe183ee88112c64429bcd749f1f8b01


class CommentForm(forms.ModelForm):

    comment  =forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows':'3',
            'placeholder':' Add comment'
        })
<<<<<<< HEAD
    ) 
    
    class Meta:
        model = Comment 
=======
    ) # only text body taken as input
    
    class Meta:
        model = Comment # connected to Comment Model
>>>>>>> 2cf088b9dfe183ee88112c64429bcd749f1f8b01
        fields = ['comment']