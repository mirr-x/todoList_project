# Create your views here.
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.db.models import Q
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required


def user_login(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password:
            if "@" in username:
                user = User.objects.filter(email=username).first()
                if user and user.check_password(password):
                    login(request, user)
                    messages.success(request, "You have successfully logged in !")
                    return redirect("home")
                else:
                    messages.error(request, "Password is incorrect !")
            else:
                user = authenticate(request, username=username, password=password)
                if user:
                    login(request, user)
                    messages.success(request, "You have successfully logged in !")
                    return redirect("home")
                else:
                    messages.error(request, "Username or password is incorrect !")
        else:
            messages.error(request, "Please enter your username and password")
    return render(request, "auth-project/login.html")


def user_signup(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        first_name = request.POST.get("first-name")
        last_name = request.POST.get("last-name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        if first_name and last_name and username and email and password:
            if not User.objects.filter(Q(username=username) | Q(email=email)).exists():
                hashed_password = make_password(password)
                user = User.objects.create(
                    email=email,
                    password=hashed_password,
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                )
                login(request, user)
                messages.success(request, "Account successfully created !")
                return redirect("home")
            else:
                messages.error(request, "This account already exists !")
        else:
            messages.error(request, "Please fill out all required fields !")
    return render(request, "auth-project/signup.html")


def user_logout(request):
    logout(request)
    return redirect("home")


def forget_password(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        email = request.POST.get("email")
        if email:
            user = get_object_or_404(User, email=email)
            token = get_random_string(40)
            expire_date = timezone.now() + timedelta(minutes=5)
            user.Token.reset_password_token = token
            user.Token.reset_password_expire = expire_date
            user.Token.save()

            link = "http://105.157.236.69:8000/change_password/{token}".format(
                token=token
            )
            body = "Your password reset link is: {link}".format(link=link)
            send_mail(
                "Password reset from to_do_list !",
                body,
                settings.EMAIL_HOST_USER,
                [email],
            )
            messages.success(request, "Email send succes !")
    return render(request, "auth-project/forget.html")


def change_password(request, token):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        password = request.POST.get("password")
        confirmPassword = request.POST.get("confirmPassword")

        if not password or not confirmPassword:
            messages.error(request, "Please fill out all required fields !")
            return render(request, "auth-project/change.html")

        user = get_object_or_404(User, Token__reset_password_token=token)

        if user.Token.reset_password_expire < timezone.now():
            messages.error(request, "Password reset link has expired !")
            return render(request, "auth-project/change.html")

        if password != confirmPassword:
            messages.error(request, "Password don't equal confirmPassword !")
            return render(request, "auth-project/change.html")

        user.password = make_password(password)
        user.Token.reset_password_token = ""
        user.Token.reset_password_expire = None
        user.Token.save()
        user.save()
        messages.success(request, "password is change !")
        return redirect("home")

    return render(request, "auth-project/change.html")


@login_required
def profile_update(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = ProfileForm(instance=request.user)
    return render(request, "auth-project/profile.html", {"form": form})
