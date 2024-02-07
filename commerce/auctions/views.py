from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User,listings,bid,watchlist,comments

def index(request):
    items=listings.objects.all()
    return render(request, "auctions/index.html",{"items":items})


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
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
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })
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
    
    
def create(request):
    if request.method == "POST":
        title=request.POST["title"]
        description=request.POST["des"]
        category=request.POST["category"]
        minimum_bid=request.POST["bid"]
        image_url=request.POST["image_url"]
        user=request.user
        item=listings(user=user,title=title,description=description,category=category,minimum_bid=minimum_bid,image_url=image_url)
        item.save()
        currentbid=bid(current_bid=minimum_bid,item=item)
        currentbid.save()
        return HttpResponseRedirect(reverse("index"))
    return render(request,"auctions/create.html")


def view(request,pk):
    if request.method == "POST":
        updated_bid=request.POST["placed_bid"]
        user=request.user
        username=user.username
        item=listings.objects.get(pk=pk)
        currently_bid=bid.objects.get(item=item)
        if username!="":
            if int(updated_bid)>currently_bid.current_bid:
                currently_bid.current_bid=int(updated_bid)
                currently_bid.updatedby=username
                currently_bid.num_of_updates=currently_bid.num_of_updates+1
                currently_bid.save()
            else:
                return HttpResponse("your bid is smaller than current_bid")
        else:
            return HttpResponse("<h1>you are not allowed to bid without signing_in</h1>")
    item=listings.objects.get(pk=pk)
    user=item.user
    updated_bid=bid.objects.get(item=item)
    return render(request,"auctions/view.html",{"title":item.title,"image_url":item.image_url,"category":item.category,"current_bid":updated_bid.current_bid,"username":user.username,"item":item})


def add_item(request,pk):
    if request.method == "POST":
        item=listings.objects.get(pk=pk)
        user=request.user
        watchlist_items=watchlist(item=item,user=user)
        watchlist_items.save()
    return HttpResponseRedirect(reverse("index"))


def watch(request):
    user=request.user
    items=watchlist.objects.filter(user=user)
    listing =[]
    for item in items:
        count=0
        for product in items:
            if item.item == product.item:
                count=count+1
        if item.item not in [x['item'] for x in listing]:
            listing.append({'item': item.item, 'count': count ,'pk':item.pk})
    return render(request,"auctions/watch.html",{"items":listing})


def delete_item(request,pk):
    if request.method == "POST":
        try:
            item=watchlist.objects.get(pk=pk)
            item.delete()
        except item.DoesNotExist:
            return HttpResponse("item not found")
    return watch(request)


def delete(request,pk):
    if request.method == 'POST':
        item=listings.objects.get(pk=pk)
        user=request.user
        username=user.username
        if item.user.username == username:
            item.delete()
        else:
            return HttpResponse(" items can be only deleted by users who listed item ")
    return HttpResponseRedirect(reverse("index"))

def add_comment(request,pk):
    item=listings.objects.get(pk=pk)
    if request.method=="POST":
        comment=request.POST["comment"]
        user=request.user
        comm=comments(comment=comment,item=item,user=user)
        comm.save()
    return HttpResponseRedirect(reverse("index"))

def view_comments(request,pk):
    item=listings.objects.get(pk=pk)
    user=item.user
    updated_bid=bid.objects.get(item=item)
    all_comments=comments.objects.filter(item=item)
    return render(request,"auctions/view.html",{"title":item.title,"image_url":item.image_url,"category":item.category,"current_bid":updated_bid.current_bid,"username":user.username,"item":item,"comments":all_comments})

def category(request):
    if request.method == "POST":
        value=request.POST["dropdown"]
        items=listings.objects.filter(category=value)
        return render(request,"auctions/index.html",{"items":items})
    return render(request,"auctions/category.html",)





