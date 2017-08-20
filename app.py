from flask import Flask, render_template
from data import Blog_posts

# Create instance of flask class.
app = Flask(__name__)

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


# Run the application
if __name__ == '__main__':
    app.run(debug=True)
