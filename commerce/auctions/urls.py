from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("all_listings", views.all_listings, name="all_listings"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<str:listing_title>", views.listing, name="listing"),
    path("newlisting", views.newlisting, name="newlisting"),
    path("useraccount",views.useraccount, name="useraccount"),
    path("watchlist",views.watchlist, name="watchlist"),
    path("edit_watchlist",views.edit_watchlist, name="edit_watchlist"),
    path("close_auction", views.close_auction, name="close_auction"),
    path("edit_listing/<int:listing_id>", views.edit_listing, name="edit_listing")
]
