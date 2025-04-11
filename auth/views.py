from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User

from auth import forms
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.

# By default Logout redirect url shows default Django Administration Logout Page
class Logout(LogoutView):
    next_page = '/'

@csrf_exempt

def login(request):
    print(f"🔹 User Authenticated? {request.user.is_authenticated}")

    if request.user.is_authenticated:
        print("✅ Already logged in. Redirecting to home.")
        return HttpResponseRedirect('/')

    loginForm = forms.LoginForm()
    error = None

    if request.method == 'POST':
        loginForm = forms.LoginForm(request.POST)
        if loginForm.is_valid():
            username = loginForm.cleaned_data['username']
            password = loginForm.cleaned_data['password']
            user = authenticate(username=username, password=password)
            print(f"🔹 Authenticated User: {user}")

            if user:
                auth_login(request, user)
                print(f"✅ User {user.username} logged in successfully!")
                if 'next' in request.GET:
                    print(f"🔹 Redirecting to {request.GET['next']}")
                    return HttpResponseRedirect(request.GET['next'])
                return HttpResponseRedirect('/')
            else:
                print("❌ Invalid credentials.")
                error = 'Invalid username or password'

    return render(request, 'auth/login.html', {"form": loginForm, "error": error})


def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')

    registerForm = forms.RegisterForm()
    addressForm = forms.AddressForm()
    error = None

    if request.method == 'POST':
        registerForm = forms.RegisterForm(request.POST)
        addressForm = forms.AddressForm(request.POST)

        if registerForm.is_valid():
            username = registerForm.cleaned_data['username']
            email = registerForm.cleaned_data['email']
            password = registerForm.cleaned_data['password']
            first_name = registerForm.cleaned_data['first_name']
            last_name = registerForm.cleaned_data['last_name']

            # ✅ FIX: Check if the user exists before creating
            if User.objects.filter(username=username).exists():
                error = "User already exists"
            else:
                try:
                    user = User.objects.create_user(
                        username=username, 
                        password=password, 
                        email=email,
                        first_name=first_name, 
                        last_name=last_name
                    )
                    if user:
                        # ✅ FIX: Save the form properly
                        registered_user = registerForm.save(commit=False)
                        registered_user.address = None  # Prevents `NoneType` error if address isn't provided
                        registered_user.save()

                        # ✅ FIX: Ensure address form is valid before saving
                        if addressForm.is_valid():
                            address = addressForm.save(commit=False)
                            address.user = registered_user
                            address.save()
                            registered_user.address = address
                            registered_user.save()

                        return HttpResponseRedirect('/auth/login')
                    else:
                        error = "User could not be created"
                except Exception as e:
                    print(e)
                    error = "An error occurred while creating the user"

    context = {
        "form": registerForm,
        "addressform": addressForm,
        "error": error
    }
    return render(request, 'auth/register.html', context)
