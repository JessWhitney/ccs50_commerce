from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Categories(models.Model):
    category_name = models.CharField(max_length=24)

    def __str__(self):
        return f"{self.category_name}"


class Bids(models.Model):
    bid = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, related_name="user_bid"
    )

    def __str__(self):
        listing = self.bid_price.first()
        listing_title = listing.title
        return f"{self.bid} by {self.user} for {listing_title}"


class Listings(models.Model):
    # Note to self: Django automatically makes a primary key called id
    title = models.CharField(max_length=64, blank=False, null=False)
    description = models.TextField()
    price = models.ForeignKey(
        Bids,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="bid_price",
    )
    # price = models.DecimalField(decimal_places=2) # could set a max amount of digits if I want
    photo = models.URLField()
    category = models.ForeignKey(
        Categories,
        on_delete=models.UniqueConstraint,
        blank=True,
        null=True,
        related_name="category",
    )
    is_active = models.BooleanField(default=True)
    seller = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name="seller"
    )
    watchlist = models.ManyToManyField(
        User, blank=True, null=True, related_name="watching"
    )

    def __str__(self):
        return f"{self.title}"


class Comments(models.Model):
    who = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_comments"
    )
    what = models.CharField(max_length=200)
    where = models.ForeignKey(
        Listings, on_delete=models.CASCADE, related_name="listing_comments"
    )

    def __str__(self):
        return f"Comment by {self.who} on {self.where}"
