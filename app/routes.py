from flask import (
    Blueprint, render_template, redirect, url_for, flash, 
    request, session, current_app
)
from flask_login import login_user
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
import os
import time

from app.forms import PostForm, LoginForm
from app.models import User
from app.models import Post
from app import db
from werkzeug.security import generate_password_hash
from app.forms import SignUpForm  # adjust path based on your project structure


main = Blueprint('main', __name__)

# Dummy admin credentials
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'password'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

@main.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(username=form.username.data).first()
            if user:
                print("✅ User found:", user.username)
                print("🔐 Hashed password in DB:", user.password)
                print("🔑 Password entered:", form.password.data)

                if check_password_hash(user.password, form.password.data):
                    login_user(user)
                    flash('Login successful!', 'success')
                    return redirect(url_for('home'))  # or your homepage
                else:
                    flash('Incorrect password.', 'danger')
            else:
                flash('User not found.', 'danger')
        except Exception as e:
            print("🔥 Exception during login:", e)
            flash('Internal server error occurred.', 'danger')
    return render_template('login.html', form=form)
    
@main.route('/logout')
def logout():
    session.pop('admin', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('main.login'))


@main.route('/admin/dashboard')
def dashboard():
    if not session.get('admin'):
        return redirect(url_for('main.login'))

    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('admin_dashboard.html', posts=posts)

@main.route('/dashboard')
def dashboard_alt():
    return render_template('dashboard_alt.html')




@main.route('/admin/create', methods=['GET', 'POST'])
def create_post():
    if not session.get('admin'):
        return redirect(url_for('main.login'))

    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data)

        # Image upload handling
        image_file = request.files.get('image')
        if image_file and image_file.filename != '':
            if allowed_file(image_file.filename):
                filename = secure_filename(image_file.filename)
                unique_filename = f"{int(time.time())}_{filename}"
                upload_path = os.path.join(current_app.root_path, 'static', 'uploads')
                os.makedirs(upload_path, exist_ok=True)
                image_file.save(os.path.join(upload_path, unique_filename))
                post.image = unique_filename
            else:
                flash('Invalid image format. Allowed: png, jpg, jpeg, gif', 'danger')
                return redirect(request.url)

        db.session.add(post)
        db.session.commit()
        flash('Post created successfully!', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('create_post.html', form=form)


@main.route('/admin/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    if not session.get('admin'):
        return redirect(url_for('main.login'))

    post = Post.query.get_or_404(post_id)
    form = PostForm(obj=post)

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data

        image_file = request.files.get('image')
        if image_file and image_file.filename != '':
            if allowed_file(image_file.filename):
                filename = secure_filename(image_file.filename)
                unique_filename = f"{int(time.time())}_{filename}"
                upload_path = os.path.join(current_app.root_path, 'static', 'uploads')
                os.makedirs(upload_path, exist_ok=True)
                image_file.save(os.path.join(upload_path, unique_filename))
                post.image = unique_filename
            else:
                flash('Invalid image format. Allowed: png, jpg, jpeg, gif', 'danger')
                return redirect(request.url)

        db.session.commit()
        flash('Post updated successfully!', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('edit_post.html', form=form, post=post)


@main.route('/admin/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    if not session.get('admin'):
        return redirect(url_for('main.login'))

    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted!', 'success')
    return redirect(url_for('main.dashboard'))


@main.route('/')
def home():
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('home.html', posts=posts)


@main.route('/post/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)


@main.route('/routes')
def show_routes():
    return '<br>'.join(f"{rule.endpoint} -> {rule.rule}" for rule in current_app.url_map.iter_rules())
