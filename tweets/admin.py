from django.contrib import admin
from tweets.models import Account, Likes, Hashtags, Tweets

admin.site.register(Account)
admin.site.register(Likes)
admin.site.register(Hashtags)
admin.site.register(Tweets)