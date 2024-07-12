from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_cors import CORS
from models import *
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import pytz

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["PROFILE_UPLOAD_FOLDER"] = "static/profile_pics"
app.config["UPLOAD_FOLDER"] = "static/uploads"

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "mp4", "avi", "mov"}

CORS(app)

db.init_app(app)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])

def index():

    if "user_id" not in session:

        return redirect(url_for("login"))

    user = get_user_by_id(session["user_id"])

    if request.method == "POST":

        user_id = session["user_id"]

        post_content = request.form.get("post")

        photo = None

        video = None

        if 'photo' in request.files:

            photo_file = request.files['photo']

            if photo_file and allowed_file(photo_file.filename):

                photo_filename = secure_filename(photo_file.filename)

                photo_path = os.path.join(app.config["UPLOAD_FOLDER"], photo_filename)

                photo_file.save(photo_path)

                photo = f"uploads/{photo_filename}"

        if 'video' in request.files:

            video_file = request.files['video']

            if video_file and allowed_file(video_file.filename):

                video_filename = secure_filename(video_file.filename)

                video_path = os.path.join(app.config["UPLOAD_FOLDER"], video_filename)

                video_file.save(video_path)

                video = f"uploads/{video_filename}"

        create_post(user_id, post_content, photo, video)

    posts = get_posts()
    
    notifs = get_follow_requests(user.id)

    central = pytz.timezone("US/Central")

    for post in posts:

        post.timestamp = post.timestamp.replace(tzinfo=pytz.utc).astimezone(central)

    return render_template("index.html", posts=posts, user=user, notifs=notifs)

@app.route("/create_post", methods=["GET", "POST"])

def create_post():

    if "user_id" not in session:

        return redirect(url_for("login"))

    if request.method == "POST":

        user_id = session["user_id"]

        post_content = request.form.get("post")

        photo = None

        video = None

        if 'photo' in request.files:

            photo_file = request.files['photo']

            if photo_file and allowed_file(photo_file.filename):

                photo_filename = secure_filename(photo_file.filename)

                photo_path = os.path.join(app.config["UPLOAD_FOLDER"], photo_filename)

                photo_file.save(photo_path)

                photo = f"uploads/{photo_filename}"

        if 'video' in request.files:

            video_file = request.files['video']

            if video_file and allowed_file(video_file.filename):

                video_filename = secure_filename(video_file.filename)

                video_path = os.path.join(app.config["UPLOAD_FOLDER"], video_filename)

                video_file.save(video_path)

                video = f"uploads/{video_filename}"

        create_post_db(user_id, post_content, photo, video)

        return redirect(url_for("index"))

    return render_template("create_post.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash(
                "Username already taken. Please choose a different username.", "error"
            )
            return redirect(url_for("register"))

        new_user = User(
            username=username, email=email, password=generate_password_hash(password)
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = get_user_by_email(email)

        if user:
            if check_password_hash(user.password, password):
                session["user_id"] = user.id
                session["username"] = user.username
                session["profile_picture"] = user.profile_picture

                return redirect(url_for("index"))

            else:
                flash("Incorrect password. Please try again.", "error")

        else:
            flash("Unrecognized email. Please try again.", "error")

    return render_template("login.html")


@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user_id", None)
    session.pop("username", None)
    session.pop("profile_picture", None)

    return redirect(url_for("login"))


@app.route("/profile/<username>", methods=["GET"])
def view_profile(username):
    user = get_user_by_username(username)

    if not user:
        return "User not found", 404

    notifs = get_follow_requests(session["user_id"])

    return render_template(
        "profile.html",
        session=session,
        user=user,
        get_follow_status=get_follow_status,
        notifs=notifs,
    )


@app.route("/edit_profile", methods=["GET", "POST"])
@app.route("/edit_profile", methods=["GET", "POST"])
def edit_profile():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user = get_user_by_id(session["user_id"])

    if request.method == "POST":
        bio = request.form.get("bio")

        profile_picture = request.files["profile_picture"]

        if profile_picture and allowed_file(profile_picture.filename):
            file_extension = profile_picture.filename.rsplit(".", 1)[1].lower()
            filename = f"{user.username}.{file_extension}"

            profile_picture_path = os.path.join(app.config["PROFILE_UPLOAD_FOLDER"], filename)
            profile_picture.save(profile_picture_path)

            user.profile_picture = f"profile_pics/{filename}"

        user.bio = bio

        db.session.commit()

        session["profile_picture"] = user.profile_picture

        return redirect(url_for("view_profile", username=user.username))

    notifs = get_follow_requests(session["user_id"])

    return render_template("edit_profile.html", user=user, notifs=notifs)


@app.route("/follow", methods=["POST"])
def follow():
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Assuming you have a way to fetch the user object

    user = get_user_by_id(session["user_id"])
    followed_id = request.args.get("user")
    followed_user = get_user_by_id(followed_id)

    if not followed_user or not user:
        return "User not found", 404

    action = request.args.get("action")

    if action == "request":
        toggle_follow(user.id, followed_id)
        flash("Follow request has been sent.", "success")

    elif action == "unfollow":
        toggle_follow(user.id, followed_id)
        flash("User has been unfollowed.", "success")

    elif action == "approve":
        approve_follow_request(followed_id, user.id)
        flash("Follow request has been approved.", "success")

    elif action == "decline":
        decline_follow_request(followed_id, user.id)
        flash("Follow request has been rejected.", "success")

    else:
        return "Invalid action", 400

    return redirect(url_for("view_profile", username=followed_user.username))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
