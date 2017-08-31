import unittest
from flask import Flask, abort, url_for
from flask_testing import TestCase
from passlib.hash import sha256_crypt
from app import db
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


class TestModels(TestBase):

    # Test the number of users in User table
    def test_user_model(self):
        self.assertEqual(User.query.count(), 2)

    # Test the number of articles in Article tab
    def test_article_model(self):
        self.assertEqual(Article.query.count(), 1)


if __name__ == '__main__':
    unittest.main()
