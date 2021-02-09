"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


DEFAULT_IMAGE = 'https://blog.nscsports.org/wp-content/uploads/2014/10/default-img.gif'
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    '''Users table'''

    __tablename__='users'

    def __repr__(self):
        return f'<User {self.first_name} {self.last_name}>'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    first_name = db.Column(db.String(20), nullable = False)
    last_name = db.Column(db.String(20), nullable = False)
    image_url = db.Column(db.Text, default = DEFAULT_IMAGE)

    posts = db.relationship('Post', backref='user', cascade='all, delete')

    def get_full_name(self):
        return self.first_name+' '+self.last_name
    
    @classmethod
    def list_users_in_order(cls):
        users = cls.query.order_by(cls.first_name).order_by(cls.last_name).all()
        return users

class Post(db.Model):
    '''Post table'''

    __tablename__='posts'

    def __repr__(self):
        return f'<Post {self.title} {self.content} {self.created_at} {self.user_id}>'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    tags = db.relationship('Tag', secondary='posts_tags', backref='posts')

class Tag(db.Model):
    '''Tag table'''

    __tablename__='tags'

    def __repr__(self):
        return f'<Tag {self.name}>'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)

class PostTag(db.Model):
    '''posts_tags table'''
    __tablename__='posts_tags'

    def __repr__(self):
        return f'<PostTag {self.post_id} {self.tag_id}>'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete='CASCADE'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)

