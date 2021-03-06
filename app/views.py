from flask import flash, redirect, url_for, session, request, render_template, abort
from passlib.hash import sha256_crypt
from functools import wraps

from app import app, db
from .models import User, Article
from .forms import RegisterForm, ArticleForm


# Decorator to check if user is logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Please login', 'danger')
            return redirect(url_for('login'))
    return wrap


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/articles')
def articles():
    # Get all articles from the db
    articles = Article.query.all()

    # If there are articles in the db
    if articles is not None:
        return render_template('articles.html', articles=articles)
    else:
        msg = 'No Articles Found'
        return render_template('articles.html', msg=msg)


# Renders a specific article
@app.route('/article/<string:id>/')
def get_article(id):

    article = Article.query.filter_by(id=id).first()

    # If the article exists in the db
    if article is not None:
        return render_template('article.html', article=article)
    else:
        abort(404)


# This a POST request to submit a register form
# Redirects to login page after successful registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Create a register form
    # Uses forms.py
    form = RegisterForm(request.form)

    # If the request method is POST and all fields are filled out
    if request.method == 'POST' and form.validate():
        # Create new user object
        user = User(name=form.name.data,
                    email=form.email.data,
                    username=form.username.data,
                    password=sha256_crypt.encrypt(str(form.password.data)))  # Encrypt password

        # If the email already exists in the database
        if User.query.filter_by(email=form.email.data).first() \
                or User.query.filter_by(username=form.username.data).first() is not None:
            error = 'username/Email already exists'
            return render_template('register.html', form=form, error=error)
        else:
            # Add user to the database
            db.session.add(user)
            db.session.commit()

            # Redirect to the login page
            flash('You are now registered and can login', 'success')
            return redirect(url_for('login'))

    # If something isn't entered correctly, reload page
    return render_template('register.html', form=form)


# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    # If the form is submitted as POST
    if request.method == 'POST':
        # Get form fields (username and password)
        username = request.form['username']
        # We want correct password to be put in database
        password_candidate = request.form['password']

        # Get specified user
        user = User.query.filter_by(username=username).first()

        # Check if user exists in the database
        if user is not None:
            # Check if password exists
            if sha256_crypt.verify(password_candidate, user.password):
                # Passwords matched - Successful login
                # Create session variables to be stored
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')

                # Check if the user is an admin
                if user.is_admin:
                    return redirect(url_for('admin_dashboard'))

                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
        else:

            # No user found
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')


# Logout the user
# User can only access /login if logged in
@app.route('/logout')
@is_logged_in
def logout():
    # Clear the session variables
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('index'))


# Renders the user dashboard page
# User can only access /dashboard if logged in
@app.route('/dashboard')
@is_logged_in
def dashboard():
    # Get only the user's articles from the db
    articles = Article.query.filter_by(author=session["username"]).all()

    # Get current user
    user = User.query.filter_by(username=session['username']).first()

    # Check if user is admin and redirect to admin dashboard
    if user.is_admin:
        return redirect(url_for('admin_dashboard'))
    else:
        # If the user has articles in the db
        if articles is not None:
            return render_template('dashboard.html', articles=articles)
        else:
            msg = 'No Articles Found'
            return render_template('dashboard.html', msg=msg)


# Add an article
# User can only access /add_article if logged in
@app.route('/add_article', methods=['GET', 'POST'])
@is_logged_in
def add_article():
    form = ArticleForm(request.form)

    if request.method == 'POST' and form.validate():
        # Create article entry from the form
        article = Article(title=form.title.data,
                          author=session['username'],
                          body=form.body.data)

        # Add article to the database
        db.session.add(article)
        db.session.commit()

        flash('Article created', 'success')
        return redirect(url_for('dashboard'))

    # If something isn't entered correctly, reload the page
    return render_template('add_article.html', form=form)


# Edit article
@app.route('/edit_article/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_article(id):

    # Get the article from the database
    article = Article.query.filter_by(id=id).first()

    # Get form
    form = ArticleForm(request.form)

    # Populate article form fields
    form.title.data = article.title
    form.body.data = article.body

    if request.method == 'POST' and form.validate():
        # set the article's fields to be the newly edited title and body
        article.title = request.form['title']
        article.body = request.form['body']

        # Commit changes to the database
        db.session.commit()

        # Get current user
        user = User.query.filter_by(username=session['username']).first()

        flash('Article updated', 'success')

        # Redirect to admin dashboard if the user is admin
        if user.is_admin:
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('dashboard'))

    # If something isn't entered correctly, reload the page
    return render_template('edit_article.html', form=form)


# Delete article
@app.route('/delete_article/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def delete_article(id):
    # Get specified article from the database
    article = Article.query.filter_by(id=id).first()

    # Delete the article
    db.session.delete(article)
    db.session.commit()

    # Get current user
    user = User.query.filter_by(username=session['username']).first()

    flash('article deleted', 'success')

    # Redirect to admin dashboard if the user is admin
    if user.is_admin:
        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('dashboard'))


# Admin dashboard view
@app.route('/admin/dashboard')
@is_logged_in
def admin_dashboard():
    # Get a potentional admin
    admin = User.query.filter_by(username=session["username"], is_admin=True).first()

    # If the logged in user is not an admin
    if admin is None:
        abort(403)

    # Get all the created articles
    articles = Article.query.all()

    # Display all the articles that users have created
    return render_template('dashboard.html', articles=articles)


# 403 forbidden error handler
@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403


# 404 page not found error handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# 500 internal error handler
@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500
