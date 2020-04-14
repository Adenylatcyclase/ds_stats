import praw
from os import getenv
from database import Post, session, User
from datetime import datetime, timedelta, date
from time import time


reddit = praw.Reddit(client_id=getenv('R_CLIENT_ID'),
                     client_secret=getenv("R_CLIENT_SECRET"),
                     user_agent='DarkSouls Data Bot')


def fetch_x_days(subreddit, days):
    target = datetime.today() - timedelta(days=days)
    flag = True
    while flag:
        for s in reddit.subreddit(subreddit).new(limit=100):
            if datetime.fromtimestamp(int(s.created_utc)) < target:
                flag = False
                break

            user = session.query(User).filter(User.name == s.author.name)
            user = user.first()

            if user is None:
                user = User(name=s.author.name)
                session.add(user)

            p = Post(title=s.title,
                     text=s.selftext,
                     user=user,
                     link=s.url,
                     num_comments=s.num_comments,
                     score=s.score,
                     r_id=s.id,
                     date=date.fromtimestamp(s.created_utc)
                     .strftime("%Y-%m-%d"),
                     updated=int(time()*1000))
        print("cycle")
        session.add(p)
        session.commit()


print("running yo")
fetch_x_days("DarkSouls2", 30)
