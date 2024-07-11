from flask import Flask, render_template, request, redirect, url_for, session, flash

from flask_cors import CORS

from werkzeug.security import generate_password_hash, check_password_hash

from werkzeug.utils import secure_filename

import os

from models import db, create_post, get_posts, create_user, get_user_by_email, add_comment, get_comments, like_post, get_likes, get_user_by_id, get_user_by_username, update_profile, User

app = Flask(__name__)

app.config['SECRET_KEY'] = 'your_secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

CORS(app)

db.init_app(app)

app.config['UPLOAD_FOLDER'] = 'static/profile_pics'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):

    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])

def index():

    if 'user_id' not in session:

        return redirect(url_for('login'))

    user = get_user_by_id(session['user_id'])

    if request.method == 'POST':

        user_id = session['user_id']

        post_content = request.form.get('post')

        create_post(user_id, post_content)

    posts = get_posts()

    return render_template('index.html', posts=posts, user=user)

@app.route('/register', methods=['GET', 'POST'])

def register():

    if request.method == 'POST':

        username = request.form.get('username')

        email = request.form.get('email')

        password = request.form.get('password')

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:

            flash('Username already taken. Please choose a different username.', 'error')

            return redirect(url_for('register'))

        new_user = User(username=username, email=email, password=generate_password_hash(password))

        db.session.add(new_user)

        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])

def login():

    if request.method == 'POST':

        email = request.form.get('email')

        password = request.form.get('password')

        user = get_user_by_email(email)

        if user:

            if check_password_hash(user.password, password):

                session['user_id'] = user.id

                session['username'] = user.username

                session['profile_picture'] = user.profile_picture  # Add profile picture to session

                return redirect(url_for('index'))

            else:

                flash('Incorrect password. Please try again.', 'error')

        else:

            flash('Unrecognized email. Please try again.', 'error')

    return render_template('login.html')
 
@app.route('/logout', methods=['POST'])

def logout():

    session.pop('user_id', None)

    session.pop('username', None)

    session.pop('profile_picture', None)

    return redirect(url_for('login'))

@app.route('/profile/<username>', methods=['GET'])

def view_profile(username):

    user = get_user_by_username(username)

    if not user:

        return "User not found", 404

    return render_template('profile.html', user=user)

@app.route('/edit_profile', methods=['GET', 'POST'])

@app.route('/edit_profile', methods=['GET', 'POST'])

def edit_profile():

    if 'user_id' not in session:

        return redirect(url_for('login'))

    user = get_user_by_id(session['user_id'])

    if request.method == 'POST':

        bio = request.form.get('bio')

        profile_picture = request.files['profile_picture']

        if profile_picture and allowed_file(profile_picture.filename):

            file_extension = profile_picture.filename.rsplit('.', 1)[1].lower()

            filename = f"{user.username}.{file_extension}"

            profile_picture_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            profile_picture.save(profile_picture_path)

            user.profile_picture = f"profile_pics/{filename}"

        user.bio = bio

        db.session.commit()

        session['profile_picture'] = user.profile_picture

        return redirect(url_for('view_profile', username=user.username))

    return render_template('edit_profile.html', user=user)

if __name__ == '__main__':

    with app.app_context():

        db.create_all()

    app.run(debug=True, use_reloader=False) 