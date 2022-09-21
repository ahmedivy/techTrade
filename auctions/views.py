from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Product, User, Bid

from .forms import BidForm, CommentForm, NewProductForm

categoriez = [
        ("iPhone", "iPhone"),
        ("Android", "Android"),
        ("Macbook", "Macbook"),
        ("GraphicCards", "GraphicCards"),
        ("Headphones", "Headphones"),
        ("SmartHome", "SmartHome"),
        ("Other", "Other"),
    ]


def index(request):
    return render(request, "auctions/index.html", {
        "products" : Product.objects.filter(status=False),
        "bids" : Bid.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create(request):
    if request.method == "POST":
        form = NewProductForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user
            data.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = NewProductForm()
        return render(request, "auctions/create.html", {"form": form})

def auctions(request, id):
    item = Product.objects.get(pk=id)
    bidform = BidForm
    commentform = CommentForm
    return render(request, "auctions/auctions.html", {"product": item, "bidform": bidform, "commentform": commentform})

def end_auction(request, id):
    if request.method == "POST":
        product = Product.objects.get(pk=id)
        product.status = True
        product.save()
        return HttpResponseRedirect(reverse("auction", args=[id]))

def watch_auction(request, id):
    if request.method == "POST":
        if "add" in request.POST:
            product = Product.objects.get(pk=id)
            product.watchers.add(request.user)
            product.save()
        else:
            product = Product.objects.get(pk=id)
            product.watchers.remove(request.user)
            product.save()
        
    return HttpResponseRedirect(reverse("auction", args=[id]))

def add_comment(request, id):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.product = Product.objects.get(pk=id)
            comment.save()
        return HttpResponseRedirect(reverse("auction", args=[id]))

def add_bid(request, id):
    
    def bid_valid(amount_):
        item = Product.objects.get(pk=id)
        bids = Bid.objects.filter(product=item)
        for bid in bids:
            if bid.amount > amount_:
                return False
        if item.startBid > amount_:
            return False

        return True
    
    if request.method == "POST":
        form = BidForm(request.POST, request.FILES)
        bid = form.save(commit=False)
        if bid_valid(bid.amount):
            bid.user = request.user
            bid.product = Product.objects.get(pk=id)
            bid.save()
        else:
            message = "Bid should must be greater than above price."
            return render(request, "auctions/auctions.html", {"product": Product.objects.get(pk=id), "bidform": BidForm, "commentform": CommentForm, "message": message})

        return HttpResponseRedirect(reverse("auction", args=[id]))

def watchlist(request):
    
    products = Product.objects.filter(watchers = request.user)
    
    return render(request, "auctions/watchlist.html", {
        "products" : products,
        "bids" : Bid.objects.all()
    })

def categories(request):

    return render(request, "auctions/categories.html", {
        "categories" : [_[1] for _ in categoriez]
    })

def category(request, category):
    return render(request, "auctions/category.html", {
        "products" : Product.objects.filter(category=category, status=False),
        "bids" : Bid.objects.all(),
        "category": category,
    })