from django.urls import path
from .views import signup, login_view, forgot_password, index, set_new_password, user_page, polls, vote_poll

urlpatterns = [
    path("", index, name="index"),
    path("signup/", signup, name="signup"),
    path("login/", login_view, name="login"),
    path("forgot-password/", forgot_password, name="forgot_password"),
    path("set-new-password/<int:user_id>/", set_new_password, name="set_new_password"),
    path("userpage/", user_page, name="user_page"),
    path("polls/", polls, name="polls"),
    path("poll/<int:poll_id>/vote/<int:choice_id>/", vote_poll, name="vote_poll"),
]
