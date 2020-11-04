from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<str:listing_title>", views.listing, name="listing"),
    path("newlisting", views.newlisting, name="newlisting"),
    path("useraccount",views.useraccount, name="useraccount"),
    path("watchlist",views.watchlist, name="watchlist"),
    path("edit_watchlist/<str:listing_title>",views.edit_watchlist, name="edit_watchlist")
]
