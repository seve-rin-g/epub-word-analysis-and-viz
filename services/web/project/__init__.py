from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)


class Book(db.Model):
    __tablename__ = "ol_books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    author = db.Column(db.String(128))

    def __init__(self, title, author):
        self.title = title
        self.author = author
        
class Word(db.Model):
    __tablename__ = "ol_words"

    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(128))

    def __init__(self, word):
        self.word = word
        
class WordBookLink(db.Model):
    __tablename__ = "ol_word_book_link"

    id = db.Column(db.Integer, primary_key=True)
    wordid = db.Column(db.Integer, db.ForeignKey('ol_words.id'))
    bookid = db.Column(db.Integer, db.ForeignKey('ol_books.id'))
    frequency = db.Column(db.Integer)

    def __init__(self, wordid, bookid):
        self.wordid = wordid
        self.bookid = bookid
        
@app.route("/")
def homepage():
    books = Book.query.order_by(Book.author.desc()).all()
    return render_template('index.html', books=books)