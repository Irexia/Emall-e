from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import login_info, SECURITY_QUESTION_CHOICES, Category


class SignupForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    age = forms.IntegerField()
    name = forms.CharField()
    email = forms.EmailField()
    phone_number = forms.CharField()
    security_question = forms.CharField()
    security_answer = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields["security_question"].widget = forms.Select(
            choices=SECURITY_QUESTION_CHOICES
        )


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class ForgotPasswordForm(forms.Form):
    username = forms.CharField()
    security_question = forms.CharField()
    security_answer = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(ForgotPasswordForm, self).__init__(*args, **kwargs)
        self.fields["security_question"].widget = forms.Select(
            choices=SECURITY_QUESTION_CHOICES
        )

    # new_password = forms.CharField(widget=forms.PasswordInput())


class ProductSearchForm(forms.Form):
    keyword = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Search by name, description, or category",
            }
        ),
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="Select category",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    min_price = forms.FloatField(
        required=False,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Min Price"}
        ),
    )
    max_price = forms.FloatField(
        required=False,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Max Price"}
        ),
    )
    # Add more fields as needed based on your model

    def filter_queryset(self, queryset):
        keyword = self.cleaned_data.get("keyword")
        category = self.cleaned_data.get("category")
        min_price = self.cleaned_data.get("min_price")
        max_price = self.cleaned_data.get("max_price")

        if keyword:
            queryset = (
                queryset.filter(name__icontains=keyword)
                | queryset.filter(description__icontains=keyword)
                | queryset.filter(category__name__icontains=keyword)
            )

        if category:
            queryset = queryset.filter(category=category)

        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        # Add more filtering logic as needed based on your model

        return queryset


class UserEditForm(forms.ModelForm):
    class Meta:
        model = login_info
        fields = [
            "username",
            "name",
            "email",
            "age",
            "phone_number",
            "security_question",
            "security_answer",
        ]


# rifa
from .models import ReviewRating


# review rating
class ReviewRatingForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ["review", "rating"]
