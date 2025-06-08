from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.forms import PostForm, LoginForm
from app.models import Post
from app import db

main = Blueprint('main', __name__)

# Dummy admin credentials
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'password'

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('admin'):
        return redirect(url_for('main.login'))

    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('admin_dashboard.html', posts=posts)


@main.route('/signup')
def signup():
    return render_template('signup.html')


@main.route('/')
def home():
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('index.html', posts=posts)

@main.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == ADMIN_USERNAME and form.password.data == ADMIN_PASSWORD:
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid login')
    return render_template('login.html', form=form)

@main.route('/admin/dashboard')
def dashboard():
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('admin/dashboard.html', posts=posts)

@main.route('/admin/create', methods=['GET', 'POST'])
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data)
        db.session.add(post)
        db.session.commit()
        flash('Post created!')
        return redirect(url_for('main.dashboard'))
    return render_template('admin/create_post.html', form=form)

@main.route('/admin/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm(obj=post)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Post updated!')
        return redirect(url_for('main.dashboard'))
    return render_template('admin/edit_post.html', form=form)

@main.route('/admin/delete/<int:post_id>')
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted!')
    return redirect(url_for('main.dashboard'))
