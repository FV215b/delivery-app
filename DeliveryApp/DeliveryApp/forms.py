from django import forms

class RegisterForm(forms.Form):
    restaurant_name = forms.CharField(widget=forms.TextInput(attrs={'size': 30}))
    phone = forms.CharField()
    address = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    repeat_password = forms.CharField(widget=forms.PasswordInput())
