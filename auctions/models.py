from django.contrib.auth.models import AbstractUser
from django.db import models

categories = [
        ("iPhone", "iPhone"),
        ("Android", "Android"),
        ("Macbook", "Macbook"),
        ("GraphicCards", "GraphicCards"),
        ("Headphones", "Headphones"),
        ("SmartHome", "SmartHome"),
        ("Other", "Other"),
    ]

class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"

class Product(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    desc = models.CharField(max_length=100)
    startBid = models.IntegerField()
    img = models.URLField(blank=True)
    category = models.CharField(max_length=30, choices=categories)
    time = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    watchers = models.ManyToManyField(User, related_name="watchlist", blank=True)

    def __str__(self):
        return f"{self.title} added for {self.startBid}$."

    class Meta:
        ordering = ['-time']

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="bids")

    def __str__(self):
        return f"{self.user.username} bid on {self.product.title} for {self.amount}."

    class Meta:
        ordering = ['-amount']

class Remark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    message = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"{self.user.username} commented on {self.product.title}"

    class Meta:
        ordering = ['-time']
    

