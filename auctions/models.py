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
    bidder = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_bids", blank=True, null=True
    )

    def __str__(self):
        listing = self.bid_price.first()
        listing_title = listing.title if listing else "Unknown"
        return f"{self.bid} for {listing_title}"


class Listings(models.Model):
    """
    Model with the overall information for each auction listing:
    - Title
    - Description
    - Seller
    - Current bid value
    - Listing category
    - Photo (optional)
    - Status of Listing (open/closed)
    """

    # Note to self: Django automatically makes a primary key called id
    title = models.CharField(max_length=64, blank=False)
    description = models.TextField(blank=True)
    price = models.ForeignKey(
        Bids,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="bid_price",
    )
    photo = models.URLField(blank=True)
    category = models.ForeignKey(
        Categories,
        on_delete=models.UniqueConstraint,
        blank=True,
        null=True,
        related_name="category",
    )
    is_active = models.BooleanField(default=True)
    seller = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="seller", blank=True, null=True
    )
    watchlist = models.ManyToManyField(
        User, blank=True, null=True, related_name="watching"
    )

    def __str__(self):
        return f"Title: {self.title} by {self.seller}"


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
