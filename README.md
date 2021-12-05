# Twitter-Neo

Twitter clone built using Django. The only routes needed are below.

'''
pip install -r requirements.txt
cd twitterneo
python manage.py runserver
'''

## Design

Created models for 'Account', 'Tweets', 'Likes', and 'Hashtags'. Created
many-to-many relationship with 'Likes' and their respective users as 
well as all the hashtags into the 'Hashtag' model.