import unittest
from flask import Flask, abort
from flask_testing import TestCase

from app import app, db
from app.models import User, Article


# The base testing class
class TestBase(TestCase):

    # Create a new Flask instance for testing
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config.update(
            SQLALCHEMY_DATABASE_URI='mysql://root:password@localhost/blogapp_db_test'
        )
        db.init_app(app)
        return app

    # Setup will be called before every test
    def setUp(self):
        db.create_all()

        # Create test admin user
        admin = User(name="admin",
                     email="admin@admin.com",
                     username="admin",
                     password="password",
                     is_admin=True)

        # Create normal user
        user = User(name="user",
                    email="email@email.com",
                    username="user",
                    password="password",
                    is_admin=False)

        # Create article
        article = Article(title="article",
                          author="user",
                          body="This is a test article.")

        # Save users to database
        db.session.add(admin)
        db.session.add(user)
        db.session.add(article)
        db.session.commit()

    # Will be called after every test
    def tearDown(self):
        db.session.remove()
        db.drop_all()


# Test the models of the database
class TestModels(TestBase):

    # Test the number of users in User table
    def test_user_model(self):

        user = User(name="user2",
                    email="emai2l@email2.com",
                    username="user2",
                    password="password",
                    is_admin=False)

        db.session.add(user)
        db.session.commit()

        self.assertEqual(User.query.count(), 3)

    # Test the number of articles in Article tab
    def test_article_model(self):

        article = Article(title="article2",
                          author="user",
                          body="This is a second test article.")

        db.session.add(article)
        db.session.commit()

        self.assertEqual(Article.query.count(), 2)


# Test the views of the app
class TestViews(TestBase):

    # Test that the home page is accessible without login
    def test_home_view(self):
        response = app.test_client().get('/')
        self.assertEqual(response.status_code, 200)

    # Test that the login page is accessible without login
    def test_login_view(self):
        response = app.test_client().get('/login')
        self.assertEqual(response.status_code, 200)

    # Test that the articles page is accessible without login
    def test_articles_view(self):
        response = app.test_client().get('/articles')
        self.assertEqual(response.status_code, 200)

    # Test that a specific article page is accessible without login
    def test_article_view(self):
        response = app.test_client().get('/article/1')
        self.assertEqual(response.status_code, 301)

    # Test that the about page is accessible without login
    def test_about_view(self):
        response = app.test_client().get('/about')
        self.assertEqual(response.status_code, 200)

    # Test that the register page is accessible without login
    def test_register_view(self):
        response = app.test_client().get('/register')
        self.assertEqual(response.status_code, 200)

    # Test that the logout link is inaccessible without login and redirects
    # to the login page
    def test_logout_view(self):
        target_url = '/logout'
        redirect_url = '/login'
        response = app.test_client().get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    # Test that the dashboard link is inaccessible without login and redirects
    # to the login page
    def test_dashboard_view(self):
        target_url = '/dashboard'
        redirect_url = '/login'
        response = app.test_client().get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    # Test that the add_article link is inaccessible without login and redirects
    # to the login page
    def test_add_article_view(self):
        target_url = '/add_article'
        redirect_url = '/login'
        response = app.test_client().get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    # Test that the edit_article link is inaccessible without login and redirects
    # to the login page
    def test_edit_article_view(self):
        target_url = '/edit_article/1'
        redirect_url = '/login'
        response = app.test_client().get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    # Test that the delete_article link is inaccessible without login and redirects
    # to the login page
    def test_delete_article_view(self):
        target_url = '/delete_article/1'
        redirect_url = '/login'
        response = app.test_client().get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    # Test that the admin dashboard link is inaccessible without login and redirects
    # to the login page
    def test_admin_dash_view(self):
        target_url = '/admin/dashboard'
        redirect_url = '/login'
        response = app.test_client().get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)


# Test the error pages of the app
class TestErrorPages(TestBase):

    # Create route to abort the request with the 404 Error
    def test_403_forbidden(self):
        @app.route('/403')
        def forbidden():
            abort(403)

        response = app.test_client().get('/403')
        self.assertEqual(response.status_code, 403)

    # Test 404 error
    def test_404_not_found(self):
        response = app.test_client().get('/nothinghere')
        self.assertEqual(response.status_code, 404)

    # Create route to abort the request with the 500 error
    def test_500_internal_server_error(self):
        @app.route('/500')
        def internal_error():
            abort(500)

        response = app.test_client().get('/500')
        self.assertEqual(response.status_code, 500)


# Run the tests
if __name__ == '__main__':
    unittest.main()
