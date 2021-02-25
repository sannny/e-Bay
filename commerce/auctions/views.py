from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import date
from datetime import datetime
from django import forms 
from .models import *


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "auctions/index.html",{
        "listings": Products.objects.filter(end_date__gte = date.today(),active=True)
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
        #first_name = request.POST["first_name"]
        #last_name = request.POST["last_name"]

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
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def sell(request):
    if request.method == "POST":
        prod_name = request.POST["name"]
        prod_image = request.POST["image_link"]
        seller_id = request.user
        description = request.POST["Description"]
        amount = request.POST["price"]
        post_date = date.today()
        end_date = datetime.strptime(request.POST["end_date"], '%Y-%m-%d').date()
        if post_date >= end_date:
            return render(request, "auctions/sell.html",{
                "message": "Invalid end date, posting date cannot be before ending date"
            })
        else:
            prod = Products(prod_name = prod_name,prod_image=prod_image,seller_id = seller_id,description=description,amount=amount,post_date=post_date,end_date=end_date)
            prod.save()
            return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/sell.html")

def prod_view(request, prod_id):
    prod = Products.objects.get(pk=prod_id)
    if request.method == 'POST':
        if request.user != prod.seller_id:
            if request.POST.get("amt",0)!=0:
                if int(request.POST["amt"]) > prod.amount:
                    if prod.end_date >= date.today():
                        product_id = prod
                        bid_date = date.today()
                        min_amount = prod.amount
                        bid_amt =int(request.POST["amt"])
                        bidder_id = request.user
                        bid = Bids(product_id=product_id, bid_date=bid_date,min_amount=min_amount,bid_amt=bid_amt,bidder_id=bidder_id)
                        bid.save()
                        prod.amount=int(request.POST["amt"])
                        prod.save()
                        return HttpResponseRedirect(reverse("Prod_page",args=(prod_id,)))
                    else:
                        return render(request,"auctions/product_page.html",{
                        "prod_ob":prod,
                        "message": "Bidding has closed for this product",
                        "comments": Comments.objects.filter(prod_id=prod)
                        })
                else:
                    return render(request,"auctions/product_page.html",{
                    "prod_ob":prod,
                    "message": "The bid amount should be more than current amount",
                    "comments": Comments.objects.filter(prod_id=prod)
                    })
            elif request.POST.get("comment","")!="":
                commenter_id = request.user
                message = request.POST["comment"]
                comment_date = date.today()
                Comm = Comments( commenter_id=commenter_id, message=message, prod_id=prod, comment_date=comment_date)
                Comm.save()
            else:
                pass
        else:
            return render(request,"auctions/product_page.html",{
                    "prod_ob":prod,
                    "message": "Seller cannot bid or review their own product",
                    "comments": Comments.objects.filter(prod_id=prod)
                    })
    return render(request,"auctions/product_page.html",{
        "prod_ob":prod,
        "comments": Comments.objects.filter(prod_id=prod)
    })

def mylist_page(request):
    return render(request, "auctions/my_listings.html",{
    "listings": Products.objects.filter(seller_id= request.user)
    })

class ProductsForm(forms.Form): 
    CHOICES=[('True',True),
         ('False',False)]
    prod_id = forms.IntegerField()
    prod_name = forms.CharField(max_length=20)
    prod_image = forms.CharField(max_length=256)
    description = forms.CharField()
    end_date = forms.DateField()
    active = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
def update_prod(request, prod_id):
    prod = Products.objects.get(pk=prod_id)
    if request.method == "POST":
        form = ProductsForm(request.POST)
        if datetime.strptime(request.POST["end_date"], '%Y-%m-%d').date() >= prod.end_date:
            prod.prod_name = form.data["prod_name"]
            prod.prod_image = form.data["prod_image"]
            prod.description = form.data["description"]
            prod.end_date = form.data["end_date"]
            prod.active = form.data["active"]
            prod.save()
            return HttpResponseRedirect(reverse("Prod_page",args=(prod_id,)))
        else:
            form.fields['prod_id'].widget = forms.HiddenInput()
            return render(request, "auctions/update.html",{
            "object":form ,
            "prod_id":prod_id,
            "message" : "You can only extend the end date"
            })
    initial_dict = {"prod_id" : prod_id,
                    "prod_name" : prod.prod_name,
                    "prod_image" : prod.prod_image,
                    "description" : prod.description,
                    "end_date" : prod.end_date,
                    "active" : prod.active
                    }
    form = ProductsForm(request.POST or None, initial = initial_dict)
    form.fields['prod_id'].widget = forms.HiddenInput()
    return render(request, "auctions/update.html",{
    "object":form ,
    "prod_id":prod_id
    })

def addToWatchlist(request,prod_id):
    prod = Products.objects.get(pk=prod_id)
    if WatchList.objects.filter(prod_id=prod,user_id=request.user):
        #message="Item already exist in your watchlist"
        return HttpResponseRedirect(reverse("watchlist"))
    elif request.user == prod.seller_id:
        return HttpResponseRedirect(reverse("watchlist"))
    else:
        #message="Item added to your watchlist"
        watchlist = WatchList(prod_id=prod, user_id=request.user)
        watchlist.save()
        return HttpResponseRedirect(reverse("watchlist"))

def watchList(request):
    return render(request,"auctions/view_watchlist.html",{
        "listings": WatchList.objects.filter(user_id=request.user)
    })