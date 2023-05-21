#ユーザ登録
from django import forms

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widwet=forms.PasswordInput)
    email = forms.EmailField()

#アカウント管理機能
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['icon', 'instagram_account', 'twitter_account', 'facebook_account', 'bio']