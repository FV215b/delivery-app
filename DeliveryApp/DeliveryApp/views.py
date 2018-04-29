from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from collections import OrderedDict
from django import forms
from .forms import RegisterForm, LoginForm, DishForm
import pyrebase, urllib

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

def login(request, template_name):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            try:
                user = authentication.sign_in_with_email_and_password(email, password)
            except:
                message = "Incorrect username or password"
                return render(request, template_name, {"message": message, "form": form})
            request.session['uid'] = str(user['idToken'])
            return HttpResponseRedirect(reverse('homepage'))
        else:
            message = "Invalid login info format"
            return render(request, template_name, {"message": message, "form": form})
    else:
        form = LoginForm()
        return render(request, template_name, {"form": form})

def homepage(request, template_name):
    try:
        id_token = request.session['uid']
        current_user = authentication.get_account_info(id_token)
        uid = current_user['users'][0]['localId']
    except:
        raise Http404

    info_orddict = database.child('Restaurants').child(uid).child('Info').get().val()
    info = dict(list(info_orddict.items()))
    dishes_orddict = database.child('Restaurants').child(uid).child('Dishes').get().val()
    if dishes_orddict is None:
        return render(request, template_name, {"info": info, "no_dishes": "So far, you don't have any dishes. Let's create one!"})
    else:
        dishes = list(dishes_orddict.items())
        return render(request, template_name, {"info": info, "dishes": dishes})

def logout(request, template_name):
    auth.logout(request)
    return render(request, "logout.html")

def register(request, template_name):
    if request.method == "POST":
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            name = form.cleaned_data["restaurant_name"]
            email = form.cleaned_data["email"]
            passwd1 = form.cleaned_data["password"]
            passwd2 = form.cleaned_data["repeat_password"]
            phone = form.cleaned_data["phone"]
            addr = form.cleaned_data["address"]
            if passwd1 == passwd2:
                try:
                    user = authentication.create_user_with_email_and_password(email, passwd1)
                except:
                    message = "Unable to create new user"
                    return render(request, template_name, {"message": message, "form": form})
                
                data = {
                    "Name": name, 
                    "Phone": phone,
                    "Address": addr,
                    "Email": email
                }
                session_id = user['idToken']
                request.session['uid'] = str(session_id)
                database.child("Restaurants").child(user['localId']).child("Info").set(data)
                return HttpResponseRedirect(reverse("homepage"))
            else:
                message = "Repeated password is not same with password"
                return render(request, template_name, {"message": message, "form": form})
        else:
            message = "Invalid register info format"
            return render(request, template_name, {"message": message, "form": form}) 
    else:
        form = RegisterForm()
        return render(request, template_name, {"form": form})
        

def create_dish(request, template_name):
    try:
        id_token = request.session['uid']
        current_user = authentication.get_account_info(id_token)
        uid = current_user['users'][0]['localId']
    except:
        raise Http404

    if request.method == "POST":
        form = DishForm(data=request.POST)
        if form.is_valid():
            dish_name = form.cleaned_data.get("dish_name")
            image = form.cleaned_data.get("image")
            ingredient = form.cleaned_data.get("ingredient") 
            flavor = form.cleaned_data.get("flavor")
            price = form.cleaned_data.get("price")
            data = {
                "Name": dish_name,
                "Image": image,
                "Ingredient": ingredient,
                "Flavor": flavor,
                "Price": price
            }
            database.child("Restaurants").child(uid).child('Dishes').push(data)
            return HttpResponseRedirect(reverse("homepage"))
        else:
            message = "Invalid dish info"
            return render(request, template_name, {"message": message, "form": form}) 
    else:
        form = DishForm()
        return render(request, template_name, {"form": form})

def dish_detail(request, template_name, dish_id):
    try:
        id_token = request.session['uid']
        current_user = authentication.get_account_info(id_token)
        uid = current_user['users'][0]['localId']
    except:
        raise Http404
    #dish_id = urllib.parse.unquote(dish_id)
   
    dish_orddict = database.child("Restaurants").child(uid).child('Dishes').child(dish_id).get().val()
    dish = dict(list(dish_orddict.items()))
    dish['dish_id'] = dish_id
    return render(request, template_name, dish)

def edit_dish(request, template_name, dish_id):
    try:
        id_token = request.session['uid']
        current_user = authentication.get_account_info(id_token)
        uid = current_user['users'][0]['localId']
    except:
        raise Http404
    #dish_id = urllib.parse.unquote(dish_id)
   
    if request.method == "POST":
        form = DishForm(data=request.POST)
        if form.is_valid():
            dish_name = form.cleaned_data.get("dish_name")
            image = form.cleaned_data.get("image")
            ingredient = form.cleaned_data.get("ingredient") 
            flavor = form.cleaned_data.get("flavor")
            price = form.cleaned_data.get("price")
            data = {
                "Name": dish_name,
                "Image": image,
                "Ingredient": ingredient,
                "Flavor": flavor,
                "Price": price
            }
            database.child("Restaurants").child(uid).child('Dishes').child(dish_id).update(data)
            return HttpResponseRedirect(reverse("dish_detail", args=(dish_id,)))
        else:
            message = "Invalid dish info"
            return render(request, template_name, {"dish_id": dish_id, "message": message, "form": form}) 
    else:
        dish_orddict = database.child("Restaurants").child(uid).child('Dishes').child(dish_id).get().val()
        dish = dict(list(dish_orddict.items()))
        form = DishForm({"dish_name": dish["Name"], "image": dish["Image"], "ingredient": dish["Ingredient"], "flavor": dish["Flavor"], "price": dish["Price"]})
        return render(request, template_name, {"dish_id": dish_id, "form": form})


def delete_dish(request, template_name, dish_id):
    try:
        id_token = request.session['uid']
        current_user = authentication.get_account_info(id_token)
        uid = current_user['users'][0]['localId']
    except:
        raise Http404
    #dish_id = urllib.parse.unquote(dish_id)
   
    dish_orddict = database.child("Restaurants").child(uid).child('Dishes').child(dish_id).get().val()
    dish = dict(list(dish_orddict.items())) 
    database.child("Restaurants").child(uid).child('Dishes').child(dish_id).remove()
    return render(request, template_name, {"dish_name": dish["Name"]})



