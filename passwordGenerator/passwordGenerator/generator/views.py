from django.shortcuts import render
from django.http import HttpResponse
import random
import time


# Create your views here.

def generatepassword(request):
    the_password = ""

    characters = list('abcdefghijklmnopqrstuvwzyz')
    uppercase = list(x.upper() for x in characters)
    if request.GET.get('uppercase'):
        characters.extend(uppercase)

    if request.GET.get('numbers'):
        characters.extend('1234567890')

    if request.GET.get('special'):
        characters.extend('~!@#$%^&*()_+}{:?><,./;[]')

    length = int(request.GET.get('length', 12))
    for x in range(length):
        the_password += random.choice(characters)

    if length > 12 or length < 6:
        the_password = "Invalid Option"

    return the_password


def abugh(request):
    return render(request, 'generator/abugh.html')


def password(request):
    return render(request, 'generator/password.html', {'password': generatepassword(request)})


def about(request):
    return HttpResponse("<h1> My name is Abu Ghalib<h1>")


def home(request):
    return render(request, 'generator/home.html')
