from datetime import datetime

from typing import List

from sqlalchemy.orm import Mapped

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(50), unique=True, nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(60), nullable=False)

    bio = db.Column(db.Text)

    profile_picture = db.Column(
        db.String(20), nullable=False, default="profile_pics/default.png"
    )

    followers: Mapped[List["Follow"]] = db.relationship(
        primaryjoin="and_(User.id==Follow.followed_id, Follow.approved==1)"
    )

    following: Mapped[List["Follow"]] = db.relationship(
        primaryjoin="and_(User.id==Follow.follower_id, Follow.approved==1)"
    )


class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    content = db.Column(db.Text, nullable=False)

    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref=db.backref("posts", lazy=True))


class Comment(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    content = db.Column(db.Text, nullable=False)

    user = db.relationship("User", backref=db.backref("comments", lazy=True))


class Like(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


class Follow(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    follower_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    followed_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    # 0 = pending, 1 = accepted
    approved = db.Column(db.Integer, default=0)

    follower: Mapped["User"] = db.relationship(
        primaryjoin="and_(Follow.follower_id==User.id)", overlaps="following"
    )

    followed: Mapped["User"] = db.relationship(
        primaryjoin="and_(Follow.followed_id==User.id)", overlaps="followers"
    )


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


def toggle_follow(follower_id, followed_id):

    existing_follow = Follow.query.filter_by(
        follower_id=follower_id, followed_id=followed_id
    ).first()

    if existing_follow:

        db.session.delete(existing_follow)

    else:

        new_follow = Follow(follower_id=follower_id, followed_id=followed_id)

        db.session.add(new_follow)

    db.session.commit()


def get_follow_requests(user_id):

    return Follow.query.filter_by(followed_id=user_id, approved=0).all()


def get_follow_status(follower_id, followed_id):

    existing_follow = Follow.query.filter_by(
        follower_id=follower_id, followed_id=followed_id
    ).first()

    if existing_follow:

        return existing_follow.approved

    return -1


def approve_follow_request(follower_id, followed_id):

    follow_request = Follow.query.filter_by(
        follower_id=follower_id, followed_id=followed_id
    ).first()

    follow_request.approved = 1

    db.session.commit()


def decline_follow_request(follower_id, followed_id):

    follow_request = Follow.query.filter_by(
        follower_id=follower_id, followed_id=followed_id
    ).first()

    db.session.delete(follow_request)

    db.session.commit()


def get_notifications(user_id):

    return get_follow_requests(user_id)


def init_db():

    db.create_all()


def __repr__(self):

    return f"User('{self.username}', '{self.email}', '{self.profile_picture}')"


def __repr__(self):

    return f"Post('{self.content}', '{self.timestamp}')"
