from django.shortcuts import render, redirect
from .models import Item, login_info, Poll, Choice
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from .forms import SignupForm, LoginForm, ForgotPasswordForm
from django.contrib import messages
from django.contrib.auth.views import LoginView


def index(request):
    items = Item.objects.all()
    return render(request, "index.html", {"items": items})

def electronic_view(request):
    return render(request, 'electronic.html')


# Create your views here.
def my_view(request):
    messages.success(request, "This is a success message.")
    messages.error(request, "This is an error message.")


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            # Check if the username already exists
            if login_info.objects.filter(
                username=form.cleaned_data["username"]
            ).exists():
                messages.error(
                    request,
                    "Username already exists. Please choose a different username.",
                )
                return render(request, "signup.html", {"form": form})

            if login_info.objects.filter(email=form.cleaned_data["email"]).exists():
                messages.error(
                    request,
                    "Email already exists. Please choose a different email or proceed to login.",
                )
                return render(request, "signup.html", {"form": form})

            user = login_info.objects.create(
                username=form.cleaned_data["username"],
                age=form.cleaned_data["age"],
                name=form.cleaned_data["name"],
                email=form.cleaned_data["email"],
                phone_number=form.cleaned_data["phone_number"],
                security_question=form.cleaned_data["security_question"],
                security_answer=form.cleaned_data["security_answer"],
            )
            user.set_password(form.cleaned_data["password"])
            user.save()
            login(request, user)

            messages.success(request, "Account created successfully!")

            return redirect("index")  # Redirect to your homepage
    else:
        form = SignupForm()
    return render(request, "signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            if not (
                login_info.objects.filter(
                    username=form.cleaned_data["username"]
                ).exists()
            ):
                messages.error(
                    request, "Username does not exist. Please Sign-up first."
                )

            # Check if the username exists in the database
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("user_page")
            else:
                # Handle incorrect username or password
                messages.error(request, "Invalid username or password.")

    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


def forgot_password(request):
    if request.method == "POST":
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            security_question = form.cleaned_data["security_question"]
            security_answer = form.cleaned_data["security_answer"]

            user = login_info.objects.filter(
                username=username,
                security_question=security_question,
                security_answer=security_answer,
            ).first()

            if user is None:
                # Handle incorrect security question or answer
                messages.error(request, "Invalid security question or answer.")
                return render(request, "forgot_password.html", {"form": form})

            # Render a new form for setting a new password
            return render(request, "set_new_password.html", {"user_id": user.id})

    else:
        form = ForgotPasswordForm()

    return render(request, "forgot_password.html", {"form": form})


def set_new_password(request, user_id):
    user = login_info.objects.get(id=user_id)

    if request.method == "POST":
        new_password = request.POST.get("new_password")

        # Set the new password (remember to handle password hashing in a real-world scenario)
        user.password = make_password(new_password)
        user.save()

        # Redirect to the login page or any other page
        return redirect("login")

    return render(request, "set_new_password.html", {"user_id": user_id})


def user_page(request):

    return render(request, "userpage.html")


def polls(request):
    if not request.user.is_authenticated:
        return redirect("login")
    polls = Poll.objects.all()
    user_choices = Choice.objects.filter(voters=request.user)
    return render(request, "polls.html", {"polls": polls, "user_choices": user_choices})


def vote_poll(request, *args, **kwargs):
    user_choice = Choice.objects.filter(
        poll_id=kwargs.get("poll_id"),
        voters=request.user,
    )
    poll = Poll.objects.get(id=kwargs.get("poll_id"))
    if len(user_choice):  # remove if user already voted
        user_choice[0].voters.remove(request.user)
        user_choice[0].save()
    # add vote
    prefered_choice = [
        choice for choice in poll.choices.all() if choice.id == kwargs.get("choice_id")
    ][0]
    prefered_choice.voters.add(request.user)
    prefered_choice.save()
    return redirect("polls")
