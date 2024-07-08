from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

def create_user(email, username, password):
    new_user = User(email=email, username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

def get_user_by_email(email):
    return User.query.filter_by(email=email).first()

def create_post(name, content):
    new_post = Post(name=name, content=content)
    db.session.add(new_post)
    db.session.commit()

def get_posts():
    return Post.query.order_by(Post.timestamp.desc()).all()

def add_comment(post_id, user_id, content):
    new_comment = Comment(post_id=post_id, user_id=user_id, content=content)
    db.session.add(new_comment)
    db.session.commit()

def get_comments(post_id):
    return Comment.query.filter_by(post_id=post_id).order_by(Comment.timestamp.asc()).all()

def like_post(post_id, user_id):
    new_like = Like(post_id=post_id, user_id=user_id)
    db.session.add(new_like)
    db.session.commit()

def get_likes(post_id):
    return Like.query.filter_by(post_id=post_id).count()
