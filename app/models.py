from app import db


# Create a User table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), index=True)
    email = db.Column(db.String(100), index=True, unique=True)
    username = db.Column(db.String(30), index=True, unique=True)
    password = db.Column(db.String(100))
    register_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    def __repr__(self):
        return '<User %r>' % self.nickname


# Create Article table
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255))
    author = db.Column(db.String(100))
    body = db.Column(db.Text)
    create_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    def __repr__(self):
        return '<Article %r>' % self.nickname
