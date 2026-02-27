from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from .wordprocessing import read_epub_file, word_frequency_analysis

app = Flask(__name__)
app.config['SECRET_KEY'] = 'replace-this-with-a-secure-random-string'
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)

import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/tmp/uploads'
ALLOWED_EXTENSIONS = {'epub'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
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
        

@app.route("/", methods=["GET"])
def homepage():
    books = Book.query.order_by(Book.author.desc()).all()
    return render_template('index.html', books=books)

@app.route("/submit", methods=["POST"])
def submit_epub():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        epub_text = read_epub_file(filepath)
        word_freq, sentence_sources = word_frequency_analysis(epub_text)
        # For now, just show the extracted text (or you can process/store it as needed)
        return render_template('index.html', books=Book.query.order_by(Book.author.desc()).all(), word_freq=word_freq, sentence_sources=sentence_sources) 
    else:
        flash('Invalid file type')
        return redirect(request.url)