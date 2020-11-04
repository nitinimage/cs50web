from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.forms import ModelForm
from django.core import serializers

from .models import User, Listing, Bid, Comment, Watchlist


def index(request):
    return render(request, "auctions/index.html" , {
        "listings" : Listing.objects.all()
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
        location = request.POST["Location"]

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
            user.location = location
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


# def watchlist(user,listing):
#     # add or remove listing from user's watchlist
#     watchlist, created = Watchlist.objects.get_or_create(user = user)
#     if listing in watchlist.listings.all():
#         watchlist.listings.remove(listing)
#         return "Removed"
#     else:
#         watchlist.listings.add(listing)
#         return "Added"
    



def listing(request, listing_title):
    listing = Listing.objects.get(title = listing_title)
    watchlist_status = False
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        watchlist, created = Watchlist.objects.get_or_create(user = user)
        if listing in watchlist.listings.all():
            watchlist_status = True

    if request.method == "POST":
        
        if 'new_bid' in request.POST:
            new_bid = request.POST["new_bid"]  
            bid_entry = Bid.objects.create(bid_value = new_bid, bidder=user, listing=listing)
            bid_entry.save()
        elif 'comment' in request.POST:
            content = request.POST["comment"]
            comment = Comment.objects.create(content=content, listing=listing, author=user)
            comment.save()
        elif 'watchlist' in request.POST:          
            if listing in watchlist.listings.all():
                watchlist.listings.remove(listing)
            else:
                watchlist.listings.add(listing)
            
        return HttpResponseRedirect(reverse("listing",args=(listing_title,)))

    # get request    
    else:
        categories = listing.category.all()
        bid = Bid.objects.filter(listing__title = listing_title).last()  
        comments = Comment.objects.filter(listing__title = listing_title)

        return render(request, "auctions/listing.html",{
            "listing" : listing,
            "categories" : categories,
            "bid" : bid,
            "comments" : comments,
            "watchlist_status" : watchlist_status
    })

def newlisting(request):
    if request.method == "POST":
        form = Listingform(request.POST)
        if form.is_valid():
            newlisting = form.save(commit=False)
            newlisting.seller = request.user
            newlisting.save()
            form.save_m2m()
            return HttpResponseRedirect(reverse("listing",args=(newlisting.title,)))
        else:
            return render(request, "auctions/newlisting.html",{
            "form": form
            })
    else:
        form = Listingform()
        return render(request, "auctions/newlisting.html",{
            "form": form
    })

def useraccount(request):
    # user_fields = ['username','first_name','last_name',
    #                 'email','location','birth_date']
    # user_data = {}
    # for field in user_fields:
    #     user_data[field] = getattr(request.user, field)
    # return render(request, "auctions/account.html",{
    #     "user_data": user_data
    # })
    if request.method == "POST":
        form = Userform(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("useraccount"))
        else:
            return render(request, "auctions/account.html",{
            "form":form
        })

    else:
        watchlist, created = Watchlist.objects.get_or_create(user = request.user)
        listings = request.user.listings.all()
        form = Userform(instance=request.user)
        return render(request, "auctions/account.html",{
            "form":form,
            "listings":listings,
            "watchlist": watchlist.listings.all()
        })






class Listingform(ModelForm):
    class Meta:
        model = Listing
        exclude = ['seller']
        #fields = '__all__'

class Userform(ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','location','birth_date']