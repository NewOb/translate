from exts import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    emil = db.Column(db.String(100),nullable=False)
    username = db.Column(db.String(50),nullable=False)
    password = db.Column(db.String(100),nullable=False)

class Translator(db.Model):
    __tablename__ = 'translator'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    emil = db.Column(db.String(100),nullable=False)
    translatorname = db.Column(db.String(50),nullable=False)
    password = db.Column(db.String(100),nullable=False)
    money = db.Column(db.Float,nullable=False)
    right = db.Column(db.Float,nullable=True)
    pay = db.Column(db.String(150),nullable=True)
    all_time = db.Column(db.Integer,nullable=True)
    right_time = db.Column(db.Integer,nullable=True)

class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(200),nullable=False)
    content  =db.Column(db.Text,nullable=False)
    paragraph_name = db.Column(db.String(50),nullable=False)
    translated = db.Column(db.Text,nullable=True)
    re_translated = db.Column(db.Text,nullable=True)
    price = db.Column(db.Float,nullable=False)
    person = db.Column(db.Integer,nullable=True)

class Result(db.Model):
    __tablename__ = 'result'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200),nullable=False)