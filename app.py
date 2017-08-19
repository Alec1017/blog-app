from flask import Flask, render_template

# Create instance of flask class.
app = Flask(__name__)


# Renders the home page
@app.route('/')
def index():
    return render_template('home.html')


# Renders the about page
@app.route('/about')
def about():
    return render_template('about.html')


# Run the application
if __name__ == '__main__':
    app.run(debug=True)
