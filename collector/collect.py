import praw
from os import getenv
from database import Post

reddit = praw.Reddit(client_id=getenv('R_CLIENT_ID'),
                     client_secret=getenv("R_CLIENT_SECRET"),
                     user_agent='DarkSouls Data Bot')

subreddit = "DarkSouls2"
count = 100

posts = []
for s in reddit.subreddit(subreddit).new(limit=count):
    p = Post(title=s.title,
             text=s.selftext,
             author=s.author,
             link=s.url,
             num_comments=s.num_comments,
             score=s.score)
