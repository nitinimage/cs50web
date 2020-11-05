from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.forms import ModelForm, modelform_factory
from django.contrib.auth.decorators import login_required


from .models import User, Listing, Bid, Comment, Watchlist, Category


def index(request):
    return render(request, "auctions/index.html" , {
        "listings" : Listing.objects.all()
    })

def all_listings(request):
    return render(request, "auctions/all_listings.html" , {
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



def listing(request, listing_title):
    listing = Listing.objects.get(title = listing_title)
    
    if request.method == "POST":      
        if 'new_bid' in request.POST:
            new_bid = request.POST["new_bid"]  
            bid_entry = Bid.objects.create(bid_value = new_bid, bidder=request.user, listing=listing)
            bid_entry.save()
        elif 'comment' in request.POST:
            content = request.POST["comment"]
            comment = Comment.objects.create(content=content, listing=listing, author=request.user)
            comment.save()      
        return HttpResponseRedirect(reverse("listing",args=(listing_title,)))

    # get request    
    else:
        categories = listing.category.all()
        comments = Comment.objects.filter(listing__title = listing_title)

        bid = Bid.objects.filter(listing__title = listing_title).last()  
        if not bid:
            min_bid = listing.starting_bid
        else:
            min_bid = max(bid.bid_value+1,listing.starting_bid)

        watchlist_status = False
        if request.user.is_authenticated:
            watchlist, created = Watchlist.objects.get_or_create(user = request.user)
            if listing in watchlist.listings.all():
                watchlist_status = True

        return render(request, "auctions/listing.html",{
            "listing" : listing,
            "categories" : categories,
            "bid" : bid,
            "min_bid" : min_bid,
            "comments" : comments,
            "watchlist_status" : watchlist_status
    })

@login_required
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

@login_required(login_url='auctions/login')
def edit_listing(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk = listing_id)
        if 'save' in request.POST:
            form = Listingform(request.POST, instance=listing)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse("listing",args=(listing.title,)))
            else:
                return render(request, "auctions/edit_listing.html",{
                    "form":form,
                    "listing_id":listing_id,
                    "listing":listing
                })
        elif 'edit_listing' in request.POST:
            form = Listingform(instance = listing)
            return render(request, "auctions/edit_listing.html",{
                "form":form,
                "listing_id":listing_id,
                "listing":listing
            })
    else:
        # redirect to index for get requests
        return HttpResponseRedirect(reverse("index"))

@login_required
def useraccount(request):
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
        listings = request.user.listings.all()
        winnings = request.user.winnings.all()
        form = Userform(instance=request.user)
        return render(request, "auctions/account.html",{
            "form":form,
            "listings":listings,
            "winnings":winnings
        })

@login_required
def edit_watchlist(request):
    #add or remove listing from watchlist
    if request.method == "POST":
        listing_title = request.POST.get("listing_title","")
        listing = Listing.objects.get(title = listing_title)
        watchlist, created = Watchlist.objects.get_or_create(user = request.user)
        if listing in watchlist.listings.all():
            watchlist.listings.remove(listing)
        else:
            watchlist.listings.add(listing)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def watchlist(request):
    watchlist, created = Watchlist.objects.get_or_create(user = request.user)
    return render(request, "auctions/watchlist.html",{
        "watchlist": watchlist.listings.all()
    })

@login_required
def close_auction(request):
    if request.method == 'POST':
        listing_title = request.POST.get("listing_title","")
        listing = Listing.objects.get(title = listing_title)
        bid = Bid.objects.filter(listing__title = listing_title).last() 
        if bid is not None:
            listing.winner = bid.bidder
        else:
            listing.winner = request.user
        listing.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def categories(request):
    if request.method == "POST":
        form = Categoryform(request.POST)
        if form.is_valid():
            newcategory = form.save()
            newcategory.save()
            return HttpResponseRedirect(reverse("categories"))
        else:
            return render(request, "auctions/categories.html",{
            "form": form
            })
    else: 
        form = Categoryform()
        categories = Category.objects.all()
        return render(request, "auctions/categories.html",{
            "categories": categories,
            "form":form
            })

def category(request, category_name):
    listings = Listing.objects.filter(category__category = category_name)
    return render(request, "auctions/category.html",{
        "listings":listings,
        "category_name": category_name
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

class Categoryform(ModelForm):
    class Meta:
        model = Category
        fields = ['category']