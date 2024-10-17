from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Categories(models.Model):
    category_name = models.CharField(max_length=24)

    def __str__(self):
        return f"{self.category_name}"


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
    price = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    photo = models.URLField(blank=True)
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="listings",
    )
    is_active = models.BooleanField(default=True)
    seller = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="seller", blank=True, null=True
    )
    watchlist = models.ManyToManyField(
        User, blank=True, related_name="watchlist_items"
    )
    publication_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "listing"
        verbose_name_plural = "listings"

    def __str__(self):
        return f"Title: {self.title} by {self.seller}"


class Bids(models.Model):
    """
    Bid model with the information about individual bids on items including the item, price, time, and bidder.
    """
    bid_amount = models.DecimalField(decimal_places=2, max_digits=8, default=0)
    bidder = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_bids", blank=True, null=True
    )
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="bids")
    bid_date = models.DateTimeField(auto_now_add=True)

    # Some metadata
    class Meta:
        verbose_name = "bid"
        verbose_name_plural = "bids"
        ordering = ["-bid_date"] # Shows more recent(?) first

    def __str__(self):
        return f"{self.bid_amount} for {self.listing} by {self.user}"



class Comments(models.Model):
    """A model to track all the comments left on various listings.
    - The comments content
    - The user who posted it
    - Date/time of publication
    - Listing associated with the comment
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    content = models.CharField(max_length=200, blank=False)
    listing = models.ForeignKey(
        Listings, on_delete=models.CASCADE)
    publication_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "comment"
        verbose_name_plural = "comments"

    def __str__(self):
        return f"Comment by {self.user} on {self.listing}"
