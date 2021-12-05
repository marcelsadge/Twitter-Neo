from django import template
from django.db import models
from django.contrib.auth.models import User

domain = template.Library()

class Hashtags(models.Model):
    code = models.AutoField(primary_key=True)
    word = models.CharField(max_length=100, null=True)

class Account(models.Model):
    twitter_name = models.CharField(max_length=50)
    twitter_user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def contains_likes(self):
        if self.get_likes == 0:
            return False
        return True

    def contains_tweets(self):
        if self.get_tweets == 0:
            return False
        return True

    @property
    def get_likes(self):
        return Likes.objects.filter(user=self.twitter_user).count()

    @property
    def get_tweets(self):
        return Tweets.objects.filter(twitter_account=self).count()

class Tweets(models.Model):
    code = models.AutoField(primary_key=True)
    twitter_account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    twitter_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    tweet = models.TextField(null=True)
    like = models.ManyToManyField(User, related_name='like', blank=True)
    hashtag = models.ManyToManyField(Hashtags, related_name='hashtag', blank=True)
    timestamp = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ['-timestamp']

    def get_author(self):
        return self.twitter_user.username

    def get_twitter_name(self):
        if self.twitter_account is None:
            return "Twitter User"
        return self.twitter_account.twitter_name

    def is_liked(self):
        if self.get_likes == 0:
            return False
        return True

    @property
    def get_likes(self):
        return Likes.objects.filter(main_tweet=self).count()

    @property
    def query_user_likes(self, user):
        return Likes.objects.filter(main_tweet=self, user=user).count()

class Likes(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    main_tweet = models.ForeignKey(Tweets, on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(auto_now=True, null=True)

    def get_main_tweet(self):
        if self is None:
            return
        if self.main_tweet is not None:
            return self.main_tweet.tweet

    def get_user(self):
        if self is None:
            return
        if self.main_tweet is not None:
            return self.main_tweet.get_author
