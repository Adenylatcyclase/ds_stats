import praw
from os import getenv
from database import Post, session, User
from datetime import date
from time import time
from sqlalchemy.sql.expression import func


reddit = praw.Reddit(client_id=getenv('R_CLIENT_ID'),
                     client_secret=getenv("R_CLIENT_SECRET"),
                     user_agent='DarkSouls Data Bot')


def fetch_last():
    return session.query(func.max(Post.r_id)).scalar()


def fetch_x_days(subreddit, days, last=None):
    param = {"before": f"t3_{last}"} if last is not None else {}
    for s in reddit.subreddit(subreddit).new(limit=1000, param=param):

        user = session.query(User).filter(User.name == s.author.name).first()

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

        session.add(p)
        session.commit()


print("running yo")
print(fetch_last())
# fetch_x_days("DarkSouls2", 30)
