from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.urls import reverse
from collections import OrderedDict
from django import forms
from .forms import RegisterForm
import pyrebase

config = {
    'apiKey': "AIzaSyDIbRYC4mXpEcqZSt626i_BpmzRJeWTk5o",
    'authDomain': "delivery-app-9167d.firebaseapp.com",
    'databaseURL': "https://delivery-app-9167d.firebaseio.com",
    'projectId': "delivery-app-9167d",
    'storageBucket': "delivery-app-9167d.appspot.com",
    'messagingSenderId': "107413486182",
}
firebase = pyrebase.initialize_app(config)
authentication = firebase.auth()
database = firebase.database()

def login(request):
    
    return render(request, "login.html")

def welcome(request):
    email = request.POST.get("email")
    passwd = request.POST.get("passwd")
    try:
        user = authentication.sign_in_with_email_and_password(email, passwd)
    except:
        message = "invalid login information!"
        return render(request, "login.html", {"message": message})
    
    session_id = user['idToken']
    request.session['uid'] = str(session_id)
    username = database.child('Restaurants').child(user['localId']).child('Info').child('Name').get().val()

    dishes_orddict = database.child('Restaurants').child(user['localId']).child('Dishes').get().val()
    dishes = list(dishes_orddict.items())
    print(dishes)

    return render(request, "welcome.html", {"name": username, "dishes": dishes})

def logout(request):
    auth.logout(request)

    return render(request, "login.html")

def register(request):
    if request.method == "POST":
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("restaurant_name")
            email = request.cleaned_data.get("email")
            passwd1 = request.cleaned_data.get("password")
            passwd2 = request.cleaned_data.get("repeat_password")
            phone = request.cleaned_data.get("phone")
            addr = request.cleaned_data.get("address")
            if passwd1 == passwd2:
                try:
                    user = authentication.create_user_with_email_and_password(email, passwd)
                except:
                    message = "Unable to create new user"
                    return render(request, "register.html", {"message": message, "form": form})
                
                data = {
                    "Name": name, 
                    "Phone": phone, 
                    "Address": addr,
                    "Email": email
                }
                database.child("Restaurants").child(user['localId']).child("Info").set(data)
                dishes_orddict = database.child('Restaurants').child(user['localId']).child('Dishes').get().val()
                dishes = list(dishes_orddict.items())

                return render(request, "welcome.html", {"name": name, "dishes": dishes})
            
            else:
                message = "Repeated passworkd is not same with password"
                return render(request, "register.html", {"message": message, "form": form})
        else:
            message = "invalid registered information"
            return render(request, "register.html", {"message": message, "form": form}) 
    else:
        form = RegisterForm()
        return render(request, "register.html", {"form": form})
        

def create_dish(request):
    
    return render(request, "create_dish.html")

def post_dish(request): 
    dish_name = request.POST.get("name")
    ingredient = request.POST.get("ingredient") 
    flavor = request.POST.get("flavor")
    price = request.POST.get("price")
    
    data = {
        "Ingredient": ingredient,
        "Flavor": flavor,
        "Price": price
    }

    id_token = request.session['uid']
    current_user = authentication.get_account_info(id_token)
    uid = current_user['users'][0]['localId']

    username = database.child('Restaurants').child(uid).child('Info').child('Name').get().val()

    dishes_orddict = database.child('Restaurants').child(user['localId']).child('Dishes').get().val()
    dishes = list(dishes_orddict.items())    

    database.child("Restaurants").child(uid).child('Dishes').child(dish_name).set(data)
    
    return render(request, "welcome.html", {"name": username, "dishes": dishes})


