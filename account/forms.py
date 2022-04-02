from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from account.models import Account

class RegForm(UserCreationForm):
    fullname = forms.CharField(   max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                 'placeholder' : 'Fullname'
                
            }
        ),
        label = 'Fullname',
        required=True
    )
    email = forms.EmailField(   max_length=80,
        widget=forms.TextInput(
            attrs={
                'type': 'email',
                'class': 'form-control',
                 'placeholder' : 'Email'
                
            }
        ),
        label = 'Email',
        required=True
    )
    username = forms.CharField(   max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder' : 'Username'
                
            }
        ),
        label = 'Username',
        required=True
    )
    phone_number = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'tel',
                'class': 'form-control',
                'placeholder':'Phone'
            }
        ),
        label = "PHONE",
         required=True
    )
    password1 = forms.CharField( max_length=30, min_length=6,label='Password', widget=forms.PasswordInput(attrs={'placeholder': "Password", 'class': 'form-control',}))
    password2 = forms.CharField( max_length=30, min_length=6,label='Confirm Password', widget=forms.PasswordInput(attrs={'placeholder': "Confirm Password", 'class': 'form-control',}))

    class Meta:
        model = Account
        fields = ['fullname','email','username','phone_number','password1','password2']





class LoginForm(forms.ModelForm):
    username = forms.CharField(   max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder' : 'Username'
                
            }
        ),
        label = 'Username',
        required=True
    )
    password = forms.CharField( max_length=30, min_length=6,label='Password', widget=forms.PasswordInput(attrs={'placeholder': "Password", 'class': 'form-control',}))


    class Meta:
        model = Account
        fields = ['username','password']

    def clean(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
            if not authenticate(username=username,password=password):
                raise forms.ValidationError('Invalid Credentials')





class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = "__all__"