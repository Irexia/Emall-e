from django.urls import path
from .views import signup, login_view, forgot_password, index, set_new_password, user_page, polls, vote_poll, electronic_view, product, cart, order, orders, checkout
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", index, name="index"),
    path("signup/", signup, name="signup"),
    path("login/", login_view, name="login"),
    path("forgot-password/", forgot_password, name="forgot_password"),
    path("set-new-password/<int:user_id>/", set_new_password, name="set_new_password"),
    path("userpage/", user_page, name="user_page"),
    path("polls/", polls, name="polls"),
    path("poll/<int:poll_id>/vote/<int:choice_id>/", vote_poll, name="vote_poll"),
    path("electronic/", electronic_view, name="electronic"),
    path("product/<int:product_id>/", product, name="product_details"),
    path("cart/", cart, name="cart"),
    path("orders", orders, name="orders"),
    path("order/<int:order_id>/", order, name="order"),
    path("checkout", checkout, name="checkout"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
