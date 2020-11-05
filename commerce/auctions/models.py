from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


class User(AbstractUser):
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.username}"


class Category(models.Model):
    category = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.category}"


class Listing(models.Model):
    title = models.CharField(max_length=15)
    description = models.TextField(max_length=250)
    image_url = models.URLField(blank=True)
    category = models.ManyToManyField(Category, blank=True, related_name='listings')
    starting_bid = models.FloatField(default=1)
    seller = models.ForeignKey(User, related_name='listings', on_delete=models.CASCADE)
    winner = models.ForeignKey(User, related_name='winnings', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    

    @property
    def is_active(self):
        if self.winner == None:
            return True
        else:
            return False

    @property
    def status(self):
        if self.winner == None:
            return 'Active'
        else:
            return 'Sold'

    @property
    def price(self):
        bid = Bid.objects.filter(listing__title = self.title).last()
        if not bid:
            return self.starting_bid
        return max(bid.bid_value,self.starting_bid)


    def __str__(self):
        return f"{self.title}"


class Bid(models.Model):
    bid_value = models.FloatField()
    bidder = models.ForeignKey(User, related_name='bids',  on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, related_name='bids', on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return f"Bid by {self.bidder}, Listing: {self.listing}, Bid Value: {self.bid_value}"


class Comment(models.Model):
    content = models.TextField()
    listing = models.ForeignKey(Listing, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='comments', on_delete=models.SET(get_sentinel_user))

    def __str__(self):
        return f"Comment on {self.listing} by {self.author}"


class Watchlist(models.Model):
    user = models.OneToOneField(User,related_name='watchlist', on_delete=models.CASCADE)
    listings = models.ManyToManyField(Listing, blank=True ,related_name='watchlists')

    def __str__(self):
        return f"{self.user}'s Watchlist'"

