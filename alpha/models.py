from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.urls import reverse

SECURITY_QUESTION_CHOICES = [
    ("q1", "What is your favorite color?"),
    ("q2", "What is the name of your first pet?"),
    ("q3", "In which city were you born?"),
]


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class login_info(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=128)
    age = models.IntegerField(blank=True, default=0)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    security_question = models.CharField(
        max_length=255, choices=SECURITY_QUESTION_CHOICES, null=True, blank=True
    )
    security_answer = models.CharField(max_length=255, null=True, blank=True)
    # birth_date = models.DateField()


class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published", blank=True, default=timezone.now)

    def __str__(self):
        return self.question


class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="choices")
    name = models.CharField(max_length=255)
    voters = models.ManyToManyField(
        login_info, related_name="voted_options", blank=True, default=[]
    )

    @property
    def count(self):
        return self.voters.count()

    def __str__(self):
        return f"{self.name} - {self.count}"


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()
    image = models.ImageField(
        upload_to="uploads/", null=True, blank=True, default="no-image.png"
    )
    quantity = models.IntegerField()
    # wishlist
    wishlist = models.CharField(default="False", max_length=50)
    # compare
    compare = models.CharField(default="False", max_length=50)
    # rating
    rating = models.FloatField(null=True)

    def __str__(self):
        return f"{self.name}"

    # added to fetch advanced-search url
    def get_absolute_url(self):
        return reverse("product_details", args=[str(self.id)])


class Order(models.Model):
    user = models.ForeignKey(login_info, on_delete=models.CASCADE)
    order_placed = models.BooleanField(default=False)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="order_items", on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"


# Chatbot
class Chatbot(models.Model):
    user = models.CharField(max_length=255)
    bot = models.CharField(max_length=255)


# review rating
class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.FloatField()
    review = models.TextField(max_length=500, null=True)

    def __str__(self):
        return f"{self.product}: {self.rating}\n{self.review}"


# Explicitly declare app_label
class Meta:
    app_label = "alpha"
