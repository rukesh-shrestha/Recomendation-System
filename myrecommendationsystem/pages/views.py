from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm,ContactUsForm
from django.db.models import Q
from django.contrib import messages
from .models import Contactus,Places,Myrating
import requests
from django.contrib.auth.decorators import login_required
from ast import literal_eval as make_tuple
import json



# Create your views here.
def home(request):
    context = Places.objects.all()
    query = request.GET.get('q')
    if query:
        contexts = Places.objects.filter(Q(name__icontains=query)).distinct()
        return render(request, 'home.html', {'context': contexts})

    return render(request,"home.html",{'context': context})



def rating(request, place_id):
    if not request.user.is_authenticated:
        return redirect("login")
    if not request.user.is_active:
        raise Http404
    places = get_object_or_404(Places, id=place_id)
    # for rating
    if request.method == "POST":
        rate = request.POST['rating']
        ratingObject = Myrating()
        ratingObject.user = request.user
        ratingObject.places = places
        ratingObject.rating = rate
        ratingObject.save()

        return redirect("home")
    return render(request, 'rating.html', {'place': places})

def about(request):
    return render(request,"aboutus.html",{})

def contact(request):
    my_form = ContactUsForm(request.GET)
    if request.method=="POST":
        my_form = ContactUsForm(request.POST)
        if my_form.is_valid():
            Contactus.objects.create(**my_form.cleaned_data)
            return redirect("contact")


    context = {"form":my_form}
    return render(request,"contactus.html",context)

def register(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully..')
            return redirect('login')
    context = {'form': form}
    return render(request,"register.html",context)

def loginuser(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username = username, password = password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,"username or password is incorrect...")
    context = {}
    return render(request,"login.html",context)

def logoutuser(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def recommend(request):
    user_id = request.user.id
    url = "http://127.0.0.1:5000/recommend"
    payload = {'user_id':user_id}
    headers = {
        'content-type': "multipart/form-data",
        'cache-control': "no-cache",

    }

    responses = requests.request("POST",url,data=payload)
    # import pdb;pdb.set_trace()
    response = json.loads(responses.text)
    respnses_tuple = make_tuple(response)
    context = list()

    for user_id in respnses_tuple:
        try:
            recommended = Places.objects.get(id=user_id)
            context.append(recommended)
        except:
            pass

    return render(request,"recommend.html",{'context': context})