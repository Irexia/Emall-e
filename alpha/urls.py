from django.urls import path
from .views import (
    signup,
    login_view,
    forgot_password,
    index,
    set_new_password,
    user_page,
    polls,
    vote_poll,
    electronic_view,
    product,
    cart,
    order,
    orders,
    product_search_view,
    edit_user_details,
    delete_user,
    custom_logout,
    chatbot,
    chatbotResponse,
)
from .views import (
    signup,
    login_view,
    forgot_password,
    index,
    set_new_password,
    user_page,
    polls,
    vote_poll,
    electronic_view,
    product,
    cart,
    order,
    orders,
    checkout,
)
from .views import (
    chatbot,
    chatbotResponse,
    wishlist,
    compare,
    go_wishlist,
    go_compare,
    go_reviewRating,
    reviewRating,
)
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

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
    path("product-search/", product_search_view, name="product_search"),
    path("edit/", edit_user_details, name="edit_user_details"),
    path("delete/", delete_user, name="delete_user"),
    path("logout/", custom_logout, name="logout"),
    path("checkout", checkout, name="checkout"),
    # chatbot
    path("chatbot/", chatbot, name="chatbot"),
    path("chatbot/chatbotResponse/", chatbotResponse, name="chatbotResponse"),
    # wishlist
    path("wishlist/", go_wishlist, name="go_wishlist"),
    path("wishlist/<int:product_id>/", wishlist, name="wishlist"),
    # compare
    path("compare/", go_compare, name="go_compare"),
    path("compare/<int:product_id>/", compare, name="compare"),
    # review rating
    path("reviewRating/", go_reviewRating, name="go_reviewRating"),
    path("reviewRating/<int:product_id>/", reviewRating, name="reviewRating"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
