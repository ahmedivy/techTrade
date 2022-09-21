from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("auctions/<str:id>", views.auctions, name="auction"),
    path("end_auctions/<str:id>", views.end_auction, name="end_auction"),
    path("watch_auctions/<str:id>", views.watch_auction, name="watch_auction"),
    path("add_comment/<str:id>", views.add_comment, name="add_comment"),
    path("add_bid/<str:id>", views.add_bid, name="add_bid"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.category, name="category"),
]
