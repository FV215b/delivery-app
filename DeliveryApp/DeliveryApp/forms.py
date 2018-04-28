from django import forms

class LoginForm(forms.Form):
    username = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

class RegisterForm(forms.Form):
    restaurant_name = forms.CharField(widget=forms.TextInput(attrs={'size': 30}))
    phone = forms.CharField(widget=forms.NumberInput())
    address = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    repeat_password = forms.CharField(widget=forms.PasswordInput())

class DishForm(forms.Form):
    dish_name = forms.CharField()
    ingredient = forms.CharField(widget=forms.TextInput(attrs={'size': 40}))
    flavor = forms.CharField()
    price = forms.CharField() 
    
