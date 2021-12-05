"""twitterneo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from tweets.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', splash, name = 'splash'),
    path('home/', homepage, name = 'home'), 
    path('login/', login, name='login'),
    path('request_login/', request_login, name='request_login'),
    path('confirm_logout/', confirm_logout, name='confirm_logout'),
    path('logout/', request_logout, name='logout_view'),
    path('register/', register, name='register'),
    path('request_register/', request_register, name='request_register'),
    path('profile/<slug:username>', profile_account, name='profile'),
    path('c_hashtag/', hashtag_page, name='hashtag_page'),
    path('hashtag/<slug:hashtag>', render_hashtags, name='render_hashtag'),
    path('tweets/', get_user, name='tweets'),
    path('tweet_view/', tweet_view, name='tweet_view'),
    path('create_tweet/', create_tweet, name='create_tweet'),
    path('confirm_delete/<slug:code>', confirm_delete, name='confirm_delete'),
    path('like_tweet/', like_tweet, name = 'like_tweet')
]
