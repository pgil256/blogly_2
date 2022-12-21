"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):

    __table__ = 'users'

    id == db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable = False)
    last_name = db.Column(db.Text, nullable = False)
    image_url = db.Column(db.Text, nullable=False)

    user_posts = db.relatiobship("Post", backref = 'user', cascade = 'all')

    @property 
    def full_name(self):

        return f'{self.first_name} {self.last_name}'

class Post(db.Model):

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_keys = True)
    title = db.Column(db.Text, nullable = False)
    content = db.Column(db.Text, nullable = False)

def connect_db(app):
    db.app = app
    db.init_app(app)