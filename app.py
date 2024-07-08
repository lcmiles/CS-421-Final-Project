from flask import Flask, render_template, request, redirect, url_for, session

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

    if request.method == 'POST':

        user_id = session['user_id']

        post_content = request.form.get('post')  

        create_post(user_id, post_content)

    posts = get_posts()

    return render_template('index.html', posts=posts)
 
 

@app.route('/register', methods=['GET', 'POST'])

def register():

    if request.method == 'POST':

        email = request.form.get('email')

        username = request.form.get('username')

        password = request.form.get('password')

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        create_user(email, username, hashed_password)

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])

def login():

    if request.method == 'POST':

        email = request.form.get('email')

        password = request.form.get('password')

        user = get_user_by_email(email)

        if user and check_password_hash(user.password, password):

            session['user_id'] = user.id

            session['username'] = user.username

            return redirect(url_for('index'))

    return render_template('login.html')

@app.route('/logout', methods=['POST'])

def logout():

    session.pop('user_id', None)

    session.pop('username', None)

    return redirect(url_for('login'))

@app.route('/profile/<username>', methods=['GET'])

def view_profile(username):

    user = get_user_by_username(username)

    if not user:

        return "User not found", 404

    return render_template('profile.html', user=user)

@app.route('/edit_profile', methods=['GET', 'POST'])

def edit_profile():

    if 'user_id' not in session:

        return redirect(url_for('login'))

    user = get_user_by_id(session['user_id'])

    if request.method == 'POST':

        bio = request.form.get('bio')

        profile_picture = request.files['profile_picture']

        if profile_picture and allowed_file(profile_picture.filename):

            filename = secure_filename(profile_picture.filename)

            profile_picture.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            profile_picture_path = f"static/profile_pics/{filename}"

            update_profile(user.id, bio, profile_picture_path)

        else:

            update_profile(user.id, bio, user.profile_picture)

        return redirect(url_for('view_profile', username=user.username))

    return render_template('edit_profile.html', user=user)

if __name__ == '__main__':

    with app.app_context():

        db.create_all()

    app.run(debug=True, use_reloader=False)