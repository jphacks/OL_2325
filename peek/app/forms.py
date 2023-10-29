from django import forms
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User




class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label   

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
        )

class PostForm(forms.Form):
    title = forms.CharField(max_length=50, required=False)
    image = forms.ImageField(required=True)
    body = forms.CharField(max_length=500,widget=forms.Textarea, required=False)
    def __init__(self, user, *args, **kwargs):
        super(PostForm,self).__init__(*args, **kwargs)

class CommentForm(forms.Form):
    body = forms.CharField(max_length=500, label='コメントする')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = " " ##labelとformの間の文字の指定(初期は:)
    