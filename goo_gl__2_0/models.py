from hashlib import md5

from flask_login import UserMixin, LoginManager
from sqlalchemy import MetaData, Table, Column, Integer, String
from sqlalchemy.orm import mapper

from goo_gl__2_0 import app
from goo_gl__2_0.decorators import add_session_decorator

login = LoginManager(app)


@login.user_loader
@add_session_decorator
def load_user(user_id, **kwargs):
    if id is None:
        return False
    session = kwargs['session']
    return session.query(User). \
        filter(User.id == int(user_id)). \
        first()


metadata = MetaData()
links_table = Table(
    'links', metadata,
    Column('id', Integer, primary_key=True),
    Column('landing', String(255)),
    Column('redirect', String(255)),
    Column('views', Integer),
    Column('userID', Integer)
)

users_table = Table(
    'users', metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String),
    Column("pwd_hash", String)
)


class Link(object):
    id = Column("id", Integer, primary_key=True)
    landing = Column("landing", String)
    redirect = Column("redirect", String)
    views = Column("views", Integer)
    userID = Column("userID", Integer)

    def __init__(self, **kwargs):
        self.landing = kwargs['landing']
        self.redirect = kwargs['redirect']
        self.views = kwargs['views']
        self.userID = kwargs['user_id']

    def __repr__(self):
        return "<Link(LAND='%s',VIEWS='%s')>" % (self.landing, self.views)


class User(UserMixin, object):
    id = Column("id", Integer, primary_key=True)
    username = Column("username", String)
    pwd_hash = Column("pwd_hash", String)

    def check_password(self, password):
        password = password.encode('utf-8')
        if self.pwd_hash == md5(password).hexdigest():
            return True
        else:
            return False

    # def set_password(seld, password):
    # password = password.encode('utf-8')
    # self.pwd_hash = md5(password).hexdigest()

    def __init__(self, **kwargs):
        self.username = kwargs['username']
        self.pwd_hash = kwargs['pwd_hash']

    def __repr__(self):
        return "<User(ID='%s',USERNAME='%s')>" % (self.username, self.pwd_hash)


mapper(Link, links_table)
mapper(User, users_table)
