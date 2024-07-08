from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
   
   id = db.Column(db.Integer, primary_key=True)
   
   username = db.Column(db.String(50), unique=True, nullable=False)
   
   email = db.Column(db.String(120), unique=True, nullable=False)
   
   password = db.Column(db.String(60), nullable=False)
   
   profile_image = db.Column(db.String(20), nullable=False, default='default.jpg')

class Post(db.Model):
   
   id = db.Column(db.Integer, primary_key=True)
   
   user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
   
   content = db.Column(db.Text, nullable=False)
   
   timestamp = db.Column(db.DateTime, default=datetime.utcnow)

   user = db.relationship('User', backref=db.backref('posts', lazy=True))


class Comment(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    content = db.Column(db.Text, nullable=False)

    user = db.relationship('User', backref=db.backref('comments', lazy=True))

class Like(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

def create_user(email, username, password):

    new_user = User(email=email, username=username, password=password)

    db.session.add(new_user)

    db.session.commit()

def get_user_by_email(email):

    return User.query.filter_by(email=email).first()

def get_user_by_username(username):

    return User.query.filter_by(username=username).first()

def get_user_by_id(user_id):

    return User.query.get(user_id)

def update_profile(user_id, bio, profile_picture):

    user = User.query.get(user_id)

    user.bio = bio

    user.profile_picture = profile_picture

    db.session.commit()

def create_post(user_id, post_content):
   
   new_post = Post(user_id=user_id, content=post_content)
   
   db.session.add(new_post)
   
   db.session.commit()

def get_posts():

    return Post.query.order_by(Post.timestamp.desc()).all()

def add_comment(post_id, user_id, content):

    new_comment = Comment(post_id=post_id, user_id=user_id, content=content)

    db.session.add(new_comment)

    db.session.commit()

def get_comments(post_id):

    return Comment.query.filter_by(post_id=post_id).all()

def like_post(post_id, user_id):

    existing_like = Like.query.filter_by(post_id=post_id, user_id=user_id).first()

    if existing_like:

        db.session.delete(existing_like)

    else:

        new_like = Like(post_id=post_id, user_id=user_id)

        db.session.add(new_like)

    db.session.commit()

def get_likes(post_id):

    return Like.query.filter_by(post_id=post_id).count()

def init_db():

    db.create_all()

def __repr__(self):
    
    return f"User('{self.username}', '{self.email}', '{self.profile_image}')"

def __repr__(self):
    
    return f"Post('{self.content}', '{self.timestamp}')"