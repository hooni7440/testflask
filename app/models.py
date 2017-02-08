from app import db
from datetime import datetime

user_posts = db.Table('user_posts',
    db.Column('user_id',db.Integer,db.ForeignKey('users.id')),
    db.Column('post_id',db.Integer,db.ForeignKey('posts.id')))

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(50), unique=False, nullable=False)
    userimg = db.Column(db.String(300),unique=False, nullable=True)
    registered_on = db.Column('registered_on' , db.DateTime)
    posting = db.relationship('PostData',secondary=user_posts,
                              backref=db.backref('users',lazy='dynamic'))

    def __init__(self,username,email,password,userimg):
        self.username = username
        self.email = email
        self.password = password
        self.userimg = userimg
        self.registered_on = datetime.utcnow()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User %r>' % (self.username)

class PostData(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150),index=True)
    content = db.Column(db.String(3000),index=True)
    username = db.Column(db.String(50), nullable=False)
    userimg = db.Column(db.String(300),unique=False, nullable=True)
    posted_on = db.Column('posted_on' , db.DateTime)

    def __init__(self,title,content,username,userimg):
        self.title = title
        self.content = content
        self.username = username
        self.userimg = userimg
        self.posted_on = datetime.utcnow()

    def __repr__(self):
        return '<%r>' % (self.id)
