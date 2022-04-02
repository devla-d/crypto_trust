from django import forms
from account.models import Account
from .models import Kyc
from django_countries.fields import CountryField


class KycForm(forms.ModelForm):

    class Meta:
        model = Kyc
        fields = ['name','number','country_issued','ssn','document_front','document_back']



class UserUpdateForm(forms.ModelForm):

    fullname = forms.CharField(   max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                 'placeholder' : 'Fullname'
                
            }
        ),
        label = 'Fullname',
        required=False
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
        required=False
    )
    gender = forms.CharField(   max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder' : 'Gender'
                
            }
        ),
        label = 'Gender',
        required=False
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
         required=False
    ) 

    city = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder':'City'
            }
        ),
        label = "City",
         required=False
    )

    zipcode = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder':'Zipcode'
            }
        ),
        label = "Zipcode",
         required=False
    )

    address = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder':'Address'
            }
        ),
        label = "Address",
         required=False
    )

    '''country = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder':'Country'
            }
        ),
        label = "Country",
         required=False
    )'''
    country = CountryField()


    class Meta:
        model = Account
        fields = ['fullname','username','gender','phone_number','city','zipcode','address','country']