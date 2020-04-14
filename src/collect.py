import praw
from os import getenv
from database import Post, session
from datetime import date
from time import time
from sqlalchemy.sql.expression import func

subreddit_list = [
    ("darksouls", 0),
    ("DarkSouls2", 1),
    ("darksouls3", 2),
    ("onebros", 3),
    ("DarkSoulsHelp", 4),
    ("darksoulspvp", 5),
    ("SummonSign", 6)
]
reddit = praw.Reddit(client_id=getenv('R_CLIENT_ID'),
                     client_secret=getenv("R_CLIENT_SECRET"),
                     user_agent='DarkSouls Data Bot')


def fetch_last(sub_id):
    t = session.query(func.max(Post.r_id)).filter(Post.sub_id == sub_id)
    return t.scalar()


def fetch_x_days(sub, sub_id, last=None):
    param = {"before": f"t3_{last}"} if last is not None else {}
    i = 0

    for s in reddit.subreddit(sub).new(limit=1000, params=param):

        # user = session.query(User).filter(User.name == s.author.name).first()

        # if user is None:
        # user = User(name=s.author.name)
        # session.add(user)

        if s.author is None:
            username = ""
            user_id = -1
        else:
            username = s.author.name
            user_id = s.author.id

        p = Post(title=s.title,
                 user_id=user_id,
                 username=username,
                 link=s.url,
                 num_comments=s.num_comments,
                 score=s.score,
                 r_id=int(s.id, 36),
                 date=date.fromtimestamp(s.created_utc)
                 .strftime("%Y-%m-%d"),
                 updated=int(time()*1000),
                 sub_id=sub_id)

        session.add(p)

        if i % 100 == 0:
            session.commit()


print("running yo")

for sub, sub_id in subreddit_list:
    last = fetch_last(sub)
    fetch_x_days(sub, sub_id, last)
    print("cycle yo")
