from django import forms

class LoginForm(forms.Form):
    username = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

class RegisterForm(forms.Form):
    restaurant_name = forms.CharField(widget=forms.TextInput(attrs={'size': 30}))
    phone = forms.DecimalField(widget=forms.NumberInput())
    address = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    repeat_password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get('password')
        repeat_password = cleaned_data.get('repeat_password')

        if password != repeat_password:
            raise forms.ValidationError("Password and Repeat password do not match.")

class DishForm(forms.Form):
    dish_name = forms.CharField()
    image = forms.CharField(widget=forms.HiddenInput(attrs={'id': 'url'}))
    ingredient = forms.CharField(widget=forms.TextInput(attrs={'size': 40}))
    flavor = forms.CharField()
    price = forms.FloatField(widget=forms.NumberInput(attrs={'step': '0.01'})) 

class StatusForm(forms.Form):
    CHOICES = [
        ('0', 'Confirmed'),
        ('1', 'Preparing'),
        ('2', 'Delivering'),
        ('3', 'Delivered'),
    ]
    update_status = forms.ChoiceField(label="Update Order Status", widget=forms.Select(attrs={'class': "form-control"}), choices=CHOICES)
