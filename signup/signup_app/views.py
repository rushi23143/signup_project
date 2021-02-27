from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.models import User


# Create your views here.
def index(request):
    return render(request, "index.html")

def login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['pass']
        print(u, p)
        user = auth.authenticate(username=u, password=p)
        print(user)
        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')
        else:
            return redirect('login')                             
    return render(request, 'login.html') 

def signup(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect('signup')
    if request.method == "POST":
        username = request.POST['username']
        firstname = request.POST['firstname']
        middlename = request.POST['middlename']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username taken!')
            return redirect('signup')
        if User.objects.filter(email=email).exists():
            messages.info(request, 'email already exist')
            return redirect('signup')
        else:
            user = User.objects.create_user(first_name=firstname, last_name=lastname, username=username, email=email, password=password)
            messages.info(request, "Successfully registered!\n login now. ")
            user.save()
            return redirect('login')               
    return render(request, "signup.html")

def dashboard(request):
    return render(request, "dashboard.html")

def logout(request):
    if not request.user.is_authenticated:
        return redirect('login')
    auth.logout(request)
    return redirect('login')
#    return render(request, "logout.html")    