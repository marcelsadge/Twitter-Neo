from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from tweets.models import Account, Tweets, Likes, Hashtags

# Create your views here.

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
    authenticate(request, user)
    Likes.objects.all().delete()
    return redirect("/home")

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
    user = User.objects.create(username=username, password = password)
    user.set_password(password)
    user.save()
    Account.objects.create(twitter_user=user, twitter_name=name)
    return redirect('/home')

def account(request, name = None):
    twitter_user = User.objects.get(username=name)
    if not twitter_user:
        return render("Error, no user with this name.")
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
    twitter_account = Account.objects.filter(twitter_user = twitter_user)
    tweets = Tweets.objects.filter(twitter_user = twitter_user)
    return render(request, "personal.html",
    {
        "accounts": twitter_account, 
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
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def delete_tweet(request):
    tweet = Tweets.objects.get(code=request.POST.get('code'))
    tweet.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def like_tweet(request):
    if 'like' in request.POST:
        tweet = Tweets.objects.get(id=request.POST.get('like'))
        tweet.like.add(request.user)
        twitter_account = Account.objects.get(twitter_user=request.user)
        l, c = Likes.objects.get_or_create(
            twitter_account=twitter_account, 
            twitter_user = request.user, 
            main_tweet=tweet)
    else:
        tweet = Tweets.objects.get(code=request.POST.get('dislike'))
        tweet.like.remove(request.user)
        Likes.objects.filter(twitter_user=request.user, main_tweet=tweet).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def render_hashtags(request, hashtag = None):
    hg = Hashtags.objects.get(word=hashtag)
    tweets = Tweets.objects.filter(code=hg.code)
    return render(request, "hashtag.html",
    {
        "hashtag": hg,
        "tweets": tweets
    })

