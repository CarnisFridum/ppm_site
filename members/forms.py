from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.contrib.auth.forms import forms
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import ProfilePic

class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}))
    first_name = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}), max_length=50)
    last_name = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}), max_length=50)
    image = forms.ImageField(label='')

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'image')

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm,self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class']='form-control'
        self.fields['username'].widget.attrs['placeholder']='Username'
        self.fields['username'].label=''

        self.fields['password1'].widget.attrs['class']='form-control'
        self.fields['password1'].widget.attrs['placeholder']='Password'
        self.fields['password1'].label=''

        self.fields['password2'].widget.attrs['class']='form-control'
        self.fields['password2'].widget.attrs['placeholder']='Repeat Password'
        self.fields['password2'].label=''

    def save(self, *args, **kwargs):
        profile = super().save(*args, **kwargs)
        ProfilePic.objects.create(user=profile, image=self.cleaned_data.get("image"))



class EditUserForm(ModelForm):
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}))
    first_name = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}), max_length=50)
    last_name = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}), max_length=50)
    image = forms.ImageField(label='')

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email', 'image')

    def __init__(self, *args, **kwargs):
        super(EditUserForm,self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class']='form-control'
        self.fields['username'].widget.attrs['placeholder']='Username'
        self.fields['username'].label=''

    def save(self, *args, **kwargs):
        profile = super().save(*args, **kwargs)

        profilePic = ProfilePic.objects.get(user=profile)
        profilePic.image = self.cleaned_data.get("image")
        profilePic.save()

