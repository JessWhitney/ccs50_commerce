from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .forms import CreateListingForm
from .models import User, Categories, Bids, Listings, Comments

def index(request):
    active_listings = Listings.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {"listings": active_listings})


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
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
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
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def listing(request, listing_id):
    try:
        listing = Listings.objects.get(pk=listing_id)
    except Listings.DoesNotExist:
        return HttpResponseRedirect(reverse("index"))
    is_watchlist = request.user.is_authenticated and (request.user in listing.watchlist.all())
    comments = Comments.objects.filter(listing=listing)
    is_seller = request.user.username == listing.seller.username
    return render(
        request,
        "auctions/listing.html",
        {
            "listing": listing,
            "is_watchlist": is_watchlist,
            "comments": comments,
            "is_seller": is_seller,
        },
    )


def categories(request):
    categories = Categories.objects.all()
    return render(request, "auctions/categories.html", {"categories": categories})

@login_required
def watchlist(request):
    # Add something to specify the user here
    # Import the watchlist of that user
    return render(request, "auctions/watchlist.html")

@login_required
def new_listing(request):
    if request.method=='POST':
        form = CreateListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            photo = form.cleaned_data['photo']
            starting_bid = form.cleaned_data['starting_bid']
            category = form.cleaned_data['category']
            category_instance = None
            if category:
                category_instance = Categories.objects.get(category_name=category)
            listing = Listings(
                title = title,
                description = description,
                price = starting_bid,
                photo = photo,
                category = category_instance,
                seller = User.objects.get(pk=request.user.id)
            )
            listing.save()
            return HttpResponseRedirect(reverse('listing', args=[listing.id]))
        else:
            return render(request, "auctions/new_listing.html", {"form": form})

    # For GET request
    return render(request, "auctions/new_listing.html", {"form": CreateListingForm()})

@login_required
def add_to_watchlist(request, listing_id):
    listing = get_object_or_404(Listings, pk=listing_id)
    listing.watchlist.add(request.user)
    return HttpResponseRedirect(reverse('listing', args=[listing.id]))

@login_required
def remove_from_watchlist(request, listing_id):
    listing = get_object_or_404(Listings, pk=listing_id)
    listing.watchlist.remove(request.user)
    return HttpResponseRedirect(reverse('listing', args=[listing.id]))

@login_required
def user_profile(request):
    """ A page to see everything associated with that user e.g. listings, watchlist etc."""
    pass

def closed_listing(request):
    pass

def bid(request):
    pass

def add_comment(request):
    pass