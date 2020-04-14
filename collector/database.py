from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

engine = create_engine(getenv("DATABASE"))
if not database_exists(engine.url):
    create_database(engine.url)

Base = declarative_base()


class PostType:
    COOP = 0
    HELP = 1
    LORE = 2
    PVP = 3
    HACKER = 4
    MISC = 5


class System:
    PC = 0
    PS4 = 1
    XBOX = 2
    UNSPECIFIED = 3


class Game:
    DS_PTD = 0
    DS_II = 1
    DS_II_SOTFS = 2
    DS_III = 3
    DSR = 4
    UNSPECIFIEDD = 5


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    text = Column(String)
    author = Column(String)
    post_type = Column(Integer)
    system = Column(Integer)
    game = Column(Integer)
    score = Column(Integer)
    num_comments = Column(Integer)
    link = Column(String)
