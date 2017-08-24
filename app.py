from flask import Flask, flash, redirect, url_for, request, render_template, session, logging
from data import Blog_posts
from flask_mysqldb import MySQL
from forms import RegisterForm
from passlib.hash import sha256_crypt
from functools import wraps


# Create instance of flask class
app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'  # MySQL root password
app.config['MYSQL_DB'] = 'blogapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Config secret key
app.secret_key = '123456'

# Initialize MYSQL
mysql = MySQL(app)

# The dummy articles from data.py
blog_posts = Blog_posts()


# Renders the home page
@app.route('/')
def index():
    return render_template('home.html')


# Renders the about page
@app.route('/about')
def about():
    return render_template('about.html')


# Renders the articles page
@app.route('/articles')
def articles():
    return render_template('articles.html', articles=blog_posts)


# Renders a specific article
@app.route('/article/<string:id>/')
def get_article(id):
    return render_template('article.html', id=id)


# This a POST request to submit a register form
# Redirects to login page after successful registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Create a register form
    # Uses forms.py
    form = RegisterForm(request.form)

    # If the request method is POST and all fields are filled out
    if request.method == 'POST' and form.validate():
        name = form.name.data
        # TODO: encrypt email address?
        email = form.email.data
        username = form.username.data
        # Encrypt the password
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create cursor (handler for mysql)
        cur = mysql.connection.cursor()

        # Execute query (add form values to user in db)
        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)",
                    (name, email, username, password))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()
        flash('You are now registered and can login', 'success')

        return redirect(url_for('login'))

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

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

        # If a user exists by that name
        if result > 0:
            # Get stored hash, searches query and looks at the first user
            data = cur.fetchone()
            # Search for the encrypted password
            password = data['password']

            # Close connection
            cur.close()

            # Compare passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passwords matched - Successfull login
                # Create session variables to be stored
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
        else:
            # Close connection
            cur.close()

            # No user found
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')


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
    return render_template('dashboard.html')


# Run the application
if __name__ == '__main__':
    app.run(debug=True)
