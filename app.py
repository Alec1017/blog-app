from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from data import Blog_posts
from flask_mysqldb import MySQL
from forms import RegisterForm
from passlib.hash import sha256_crypt

# Create instance of flask class
app = Flask(__name__)

# Config secret key
app.secret_key = '123456'

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'blogapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Init MYSQL
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


# This a POST request to submit form
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Create a register form variable
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        # Encrypt the password
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create cursor (handler for mysql)
        cur = mysql.connection.cursor()

        # Execute query
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
    if request.method == 'POST':
        return "hello"
    return render_template('login.html')


# Run the application
if __name__ == '__main__':
    app.run(debug=True)
