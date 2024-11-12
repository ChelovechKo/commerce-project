from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse

from .models import User, Listing, Watchlist, Category, Bid, Comment
from .forms import ListingForm

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

def logout_view(request):
    logout(request)
    return redirect(reverse("index"))

def signup_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        fraction = request.POST["fraction"]
        avatar = request.FILES.get("avatar")

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/signup.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.fraction = fraction
            if avatar:
                user.avatar = avatar
            user.save()
        except IntegrityError:
            return render(request, "auctions/signup.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return redirect(reverse("index"))
    else:
        return render(request, "auctions/signup.html")

def index(request):
    '''Displays all active listings'''
    active_listings = Listing.objects.filter(is_active=True)

    return render(request, "auctions/index.html", {
        "active_tab": "active_listings",
        "listings": active_listings,
    })

def categories_view(request, category_id=None):
    ''' If a category is selected,
        then we display active listings of this category,
        if the category is not selected,
        then we display all active listings'''

    categories = Category.objects.all()
    if category_id:
        selected_category = get_object_or_404(Category, id=category_id)
        listings = Listing.objects.filter(category=selected_category, is_active=True)
    else:
        selected_category = None
        listings = Listing.objects.filter(is_active=True)
    return render(request, "auctions/categories.html", {
        "active_tab": "categories",
        "categories": categories,
        "listings": listings,
        "selected_category": selected_category,
    })

def watchlist_view(request):
    '''Displays listings that the user has added to their watchlist'''
    watchlist_listings = Listing.objects.none()
    if request.user.is_authenticated:
        watchlist_entries = Watchlist.objects.filter(user=request.user)
        listing_ids = [entry.listing.id for entry in watchlist_entries]
        watchlist_listings = Listing.objects.filter(id__in=listing_ids)

    return render(request, "auctions/watchlist.html", {
        "active_tab": "watchlist",
        "listings": watchlist_listings,
    })

def create_listing_view(request):
    '''Create new listing
        Starting price automatically becomes the first bid
    '''
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            new_listing = form.save(commit=False)
            new_listing.user_create = request.user
            new_listing.save()

            # Create the first = new_listing.price
            Bid.objects.create(user=request.user, listing=new_listing, price=new_listing.price)

            return redirect(reverse("index"))
    else:
        form = ListingForm()

    return render(request, "auctions/create_listing.html", {
        "active_tab": "create_listing",
        "form": form
    })

def listing_page_view(request, listing_id):
    '''Detailed Listing info'''
    listing = get_object_or_404(Listing, id=listing_id)
    bid_count = listing.bids.all().count() - 1
    last_bid = listing.bids.all().latest('create_date')

    is_watchlisted = False
    comments = listing.comments.order_by('-create_date')

    if request.user.is_authenticated:
        is_watchlisted = Watchlist.objects.filter(user=request.user, listing=listing).exists()

    #message for user
    if bid_count == 0:
        message = 'Place the first bid.'
    elif last_bid.user == request.user:
        message = 'Your bid is the current bid.'
    else:
        message = 'The current bid is not yours. Place your bid.'

    # Проверка на отправку формы ставки
    if request.method == "POST":
        new_bid_price = request.POST["bid_price"]
        if new_bid_price:
            try:
                new_bid_price = int(new_bid_price)
                if new_bid_price > last_bid.price:
                    Bid.objects.create(user=request.user, listing=listing, price=new_bid_price)
                    listing.price = new_bid_price
                    listing.save()
                    return redirect('listing_page', listing_id=listing.id)
                else:
                    messages.error(request, "The new bid must be higher than the current one or than the starting price.")
            except ValueError:
                messages.error(request, "Please enter a valid bid amount.")

    return render(request, "auctions/listing_page.html", {
        "listing": listing,
        "comments": comments,
        "is_watchlisted": is_watchlisted,
        'message': message,
        "bid_count": bid_count,
        "max_price": last_bid.price + 1
    })

@login_required
def add_to_watchlist_view(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    Watchlist.objects.get_or_create(user=request.user, listing=listing)
    return redirect('listing_page', listing_id=listing_id)

@login_required
def remove_from_watchlist_view(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    Watchlist.objects.filter(user=request.user, listing=listing).delete()
    return redirect('listing_page', listing_id=listing_id)


@login_required
def add_comment_view(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)

    if request.method == "POST":
        description = request.POST.get("comment_text")
        if description:
            Comment.objects.create(
                description=description,
                listing=listing,
                user=request.user
            )

    return redirect('listing_page', listing_id=listing.id)

@login_required
def close_auction_view(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)

    if listing.user_create != request.user:
        return redirect('listing_page', listing_id=listing.id)

    last_bid = listing.bids.all().latest('create_date')
    if last_bid:
        listing.user_win = last_bid.user
    listing.is_active = False
    listing.save()

    return redirect('listing_page', listing_id=listing.id)