from django.shortcuts import render, redirect
from .models import Item, login_info, Poll, Choice, Product, Order, OrderItem, Category
from .models import Item, login_info, Poll, Choice, Product, Order, OrderItem, Voucher, Chatbot
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from .forms import SignupForm, LoginForm, ForgotPasswordForm, ProductSearchForm, UserEditForm
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from .chatbot.train import train
from django.http import HttpResponse


# def index(request):
#     products = Product.objects.all()
#     return render(request, "index.html", {"products": products})
def index(request):
    # Your existing logic for fetching products
    products = Product.objects.all()

    # Add the leaderboard functionality
    leaderboard_users = Order.objects.values('user').annotate(total_orders=Count('id')).filter(order_placed=True).order_by('-total_orders')[:5]

    # Fetch login_info instances for each user
    leaderboard_users_info = [login_info.objects.get(id=user['user']) for user in leaderboard_users]

    # Set is_index_page to True
    is_index_page = True

    # Include is_index_page in the context
    context = {
        "products": products,
        "leaderboard_users": zip(leaderboard_users_info, leaderboard_users),
        "is_index_page": is_index_page,
    }

    return render(request, "index.html", context)

# def index(request):
#     # Your existing logic for fetching products
#     products = Product.objects.all()

#     # Add the leaderboard functionality
#     leaderboard_users = Order.objects.values('user').annotate(total_orders=Count('id')).filter(order_placed=True).order_by('-total_orders')[:5]

#     # Fetch login_info instances for each user
#     leaderboard_users_info = [login_info.objects.get(id=user['user']) for user in leaderboard_users]
#     is_index_page = True

#     return render(request, "index.html", {"products": products, "leaderboard_users": zip(leaderboard_users_info, leaderboard_users)})

def electronic_view(request):
    return render(request, "electronic.html")


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


def product(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, "product.html", {"product": product})


def cart(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login")

    order = Order.objects.filter(user=request.user, order_placed=False).first()

    if not order:
        order = Order.objects.create(user=request.user)

    items = []
    for item in order.items.all():
        items.append(
            {
                **model_to_dict(item),
                "price": item.product.price,
                "product": {
                    **model_to_dict(item.product),
                    "category": model_to_dict(item.product.category),
                },
            }
        )
    vouchers = order.vouchers.all()
    print("vouchers", items)

    if request.GET.get("action") == "add":
        try:
            if (
                Product.objects.get(id=request.GET.get("product_id")).quantity
                - int(request.GET.get("quantity"))
                < 0
            ):
                request.session["error"] = (
                    "Product is out of stock. Remaining quantity: "
                    + str(
                        Product.objects.get(id=request.GET.get("product_id")).quantity
                    )
                )
                return redirect("cart")
            order.items.create(
                product=Product.objects.get(id=request.GET.get("product_id")),
                quantity=request.GET.get("quantity"),
            )
            return redirect("cart")
        except Exception as e:
            print(e)

    return render(
        request,
        "cart.html",
        {
            "order": order,
            "error": request.session.pop("error", None),
            "items": items,
            "vouchers": vouchers,
        },
    )


import qrcode  # pip install qrcode pillow
import base64
from io import BytesIO


def generate_qr_code(url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    encoded_image = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return encoded_image


import json
from django.http import HttpResponse

from functools import reduce

def order(request, *args, **kwargs):

    if not request.user.is_authenticated:
        return redirect("login")

    order = Order.objects.filter(id=kwargs.get("order_id")).first()

    if not order:
        request.session["error"] = "Order does not exist"
        return redirect(request.META.get("HTTP_REFERER"))

    if request.GET.get("action") == "apply_voucher":
        voucher_code = request.GET.get("voucher_code")
        voucher = Voucher.objects.filter(code=voucher_code).first()
        if voucher and voucher.is_valid():
            order.vouchers.add(voucher)
            order.save()
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            request.session["error"] = "Invalid voucher code"
            return redirect(request.META.get("HTTP_REFERER"))

    if request.GET.get("action") == "update" or request.GET.get("action") == "checkout":
        # update quantities
        if request.GET.get("items"):
            order_items = json.loads(request.GET.get("items"))
            print(order_items)
            for item in order.items.all():
                item.quantity = int(
                    [x for x in order_items if x.get("id") == item.id][0].get(
                        "quantity"
                    )
                )
                if item.quantity > item.product.quantity:
                    request.session["error"] = (
                        "Not enough in stock. Remaining quantity of "
                        + item.product.name
                        + ": "
                        + str(item.product.quantity)
                    )
                    return redirect(request.META.get("HTTP_REFERER"))
                item.save()
        if request.GET.get("order"):
            try:
                print(json.loads(request.GET.get("order")))
                updated_order = json.loads(request.GET.get("order"))
                order.address = updated_order["address"]
                order.payment = updated_order["payment"]
                order.redeemed_points = updated_order["redeemed_points"]
                order.save()
            except Exception as e:
                print(e)
                return HttpResponse(e, status=500)
        if request.GET.get("action") == "checkout":
            return redirect("/checkout")
        else:
            return redirect(request.META.get("HTTP_REFERER"))
    if request.GET.get("action") == "remove_item":
        try:
            order.items.filter(id=request.GET.get("item_id")).delete()
            return redirect("/cart")
        except Exception as e:
            print(e)
            return HttpResponse(e, status=500)

    if request.GET.get("action") == "place":
        if order.items.count() == 0:
            print("Cart is empty")
            request.session["error"] = "Cart is empty"
            return redirect(request.META.get("HTTP_REFERER"))

        try:
            cost = 0
            for item in order.items.all():
                cost += item.quantity * item.product.price
                item.product.quantity -= item.quantity
                item.product.save()
            for voucher in order.vouchers.all():
                voucher.current_usage += 1
                voucher.save()

            request.user.points -= order.redeemed_points
            request.user.points += cost / 10
            request.user.save()
            order.order_placed = True
            order.save()
            return redirect("/order/" + str(order.id))
        except Exception as e:
            print(e)
            request.session["error"] = "Error: " + str(e)
            return redirect(request.META.get("HTTP_REFERER"))

    order = Order.objects.filter(id=kwargs.get("order_id")).first()

    items = []
    for item in order.items.all():
        items.append(
            {
                **model_to_dict(item),
                "price": item.product.price,
                "product": {
                    **model_to_dict(item.product),
                    "category": model_to_dict(item.product.category),
                },
            }
        )
    vouchers = order.vouchers.all()

    return render(
        request,
        "order.html",
        {
            "order": order,
            "items": items,
            "vouchers": vouchers,
            "qr_code": generate_qr_code(
                request.build_absolute_uri("/order/" + str(order.id))
            ),
            "error": request.session.pop("error", None),
        },
    )


def orders(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login")
    
    orders = Order.objects.filter(user=request.user)
    return render(request, "orders.html", {'orders': orders})
def checkout(request, *args, **kwargs):
    order = Order.objects.filter(user=request.user, order_placed=False).first()

    if not order:
        request.session["error"] = "Order does not exist"
        return redirect("/cart")

    if order.items.count() == 0:
        print("Cart is empty")
        request.session["error"] = "Cart is empty"
        return redirect("/cart")

    items = []
    for item in order.items.all():
        items.append(
            {
                **model_to_dict(item),
                "price": item.product.price,
                "product": {
                    **model_to_dict(item.product),
                    "category": model_to_dict(item.product.category),
                },
            }
        )
    vouchers = order.vouchers.all()

    return render(
        request,
        "checkout.html",
        {
            "order": order,
            "items": items,
            "vouchers": vouchers,
            "error": request.session.pop("error", None),
        },
    )

# advanced search
def product_search_view(request):
    queryset = Product.objects.all()
    form = ProductSearchForm(request.GET)

    if form.is_valid():
        queryset = form.filter_queryset(queryset)

    context = {
        'form': form,
        'results': queryset,
    }

    return render(request, 'product_search.html', context)

def edit_user_details(request):
    user = request.user
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_page')  # Redirect to profile page after successful update
    else:
        form = UserEditForm(instance=user)
    return render(request, 'edit_user_details.html', {'form': form})

@login_required
def delete_user(request):
    user = request.user
    if request.method == 'POST':
        user.delete()
        return redirect('index')  # Redirect to home page after deletion
    return render(request, 'delete_confirmation.html')

from django.shortcuts import redirect
from django.contrib.auth import logout

def custom_logout(request):
    logout(request)
    # Redirect to desired URL after logout
    return redirect('index')  # Replace 'index' with the name of your desired URL pattern
    return render(request, "orders.html", {"orders": orders})


from django.forms.models import model_to_dict



def chatbot(request):

    chats = train()

    for i in range(len(chats)):
        if i % 2 == 0:
            Chatbot.objects.get_or_create(user=chats[i], bot=chats[i + 1])

    return render(request, "chatbot.html")


def chatbotResponse(request):
    userMessage = request.GET.get("userMessage")
    # chatbotResponse = str(bot.get_response(userMessage))

    try:
        chatbotRes = Chatbot.objects.get(user=userMessage)
        return HttpResponse(chatbotRes.bot)
    except:
        return HttpResponse("Unfortunately, I do not have that information")


# chatbot
