from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as log, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from tweets.models import Account, Tweets, Likes, Hashtags

def splash(request):
    if request.user.is_authenticated:
        return redirect("/home")
    return render(request, "splash.html")

def login(request):
    return render(request, "login.html")

def request_login(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(username=username, password=password)
    if user is None:
        return redirect("/login")
    else:
        log(request, user)
        Likes.objects.all().delete()
        return redirect("/home")

@login_required
def confirm_logout(request):
    return render(request, "confirmlogout.html")

@login_required
def request_logout(request):
    logout(request)
    return redirect("/")

def register(request):
    return render(request, "register.html")

def request_register(request):
    username = request.POST["username"]
    password = request.POST["password"]
    name = request.POST["name"]
    if not Account.objects.filter(twitter_user__username=username):
        user = User.objects.create(username=username, password=password)
        user.set_password(password)
        user.save()
        Account.objects.create(twitter_user=user, twitter_name=name)
        log(request, user)
        Likes.objects.all().delete()
        return redirect('/home')
    else:
        return redirect('/register')

def confirm_delete(request, code):
    tweet = Tweets.objects.get(code=code)
    tweet.delete()
    return render(request, "confirmdelete.html")

def profile_account(request, username):
    if not User.objects.get(username=username):
        return render("Error, no user with this name.")
    twitter_user = User.objects.get(username=username)
    twitter_account = Account.objects.get(twitter_user=twitter_user)
    tweets = Tweets.objects.filter(twitter_user=twitter_user)
    return render(request, "user.html",
    {
        "accounts": twitter_account, 
        "users": twitter_user,
        "tweets": tweets
    })

def get_user(request):
    twitter_user = request.user
    twitter_account = Account.objects.filter(twitter_user=twitter_user)
    tweets = Tweets.objects.filter(twitter_user=twitter_user)
    return render(request, "personal.html",
    {
        "account": twitter_account, 
        "users": twitter_user,
        "tweets": tweets
    })

def homepage(request):
    twitter_user = request.user
    twitter_account = Account.objects.all()
    tweets = Tweets.objects.all()
    return render(request, "homepage.html", 
    {
        "accounts": twitter_account, 
        "users": twitter_user,
        "tweets": tweets
    })

def tweet_view(request):
    return render(request, "newtweet.html")

def create_tweet(request):
    if request.method == 'POST':
        post = request.POST['tweet']
        tweet = Tweets.objects.create(
            twitter_account = Account.objects.get(twitter_user=request.user), 
            twitter_user = request.user, 
            tweet=post)
        tokens = tweet.tweet.split(" ")
        for count, word in enumerate(tokens):
            if '#' in word:
                word = word[1:]
                if not Hashtags.objects.filter(word=word).exists():
                    ht= Hashtags.objects.create(word=word)
                else:
                    ht = Hashtags.objects.get(word=word)
                tweet.hashtag.add(ht)
                tokens[count] = '<a href="' + '/.' + '/hashtag/' + word + '">#' + word + '</a>'
        join = ' '.join(tokens)
        setattr(tweet, 'tweet', join)
        tweet.save()
    return redirect('/home')

def like_tweet(request):
    if 'like' in request.POST:
        tweet = Tweets.objects.get(code=request.POST.get('like'))
        tweet.like.add(request.user)
        twitter_account = Account.objects.get(twitter_user=request.user)
        l, c = Likes.objects.get_or_create(
            account=twitter_account, 
            user = request.user, 
            main_tweet=tweet)
    else:
        tweet = Tweets.objects.get(code=request.POST.get('dislike'))
        tweet.like.remove(request.user)
        Likes.objects.filter(user=request.user, main_tweet=tweet).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def hashtag_page(request):
    hashtags = Hashtags.objects.all()
    return render(request, "hashtagdirectory.html", 
    {
        "hashtags": hashtags
    })

def render_hashtags(request, hashtag = None):
    hashtag = Hashtags.objects.get(word=hashtag)
    tweets = Tweets.objects.filter(hashtag__code=hashtag.code)
    return render(request, "hashtag.html",
    {
        "hashtag": hashtag,
        "tweets": tweets
    })

