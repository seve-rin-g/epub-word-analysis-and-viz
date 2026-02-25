from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'replace-this-with-a-secure-random-string'
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)

import ebooklib
from ebooklib import epub
import re

import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/tmp/uploads'
ALLOWED_EXTENSIONS = {'epub'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def read_epub_file(filepath):
    book = epub.read_epub(filepath)
    # Example: extract all text from the epub
    text_content = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            text_content.append(item.get_content().decode('utf-8', errors='ignore'))
    print(f"text content = {text_content}")
    return '\n'.join(text_content)

def word_frequency_analysis(alltext):
    # Simple word frequency analysis using regex to split words
    alltext = re.sub(r'<[^>]+>', '', alltext)     # remove html tags
    words = re.findall(r'\b\w+\b', alltext.lower())
    frequency = {}
    for word in words:
        frequency[word] = frequency.get(word, 0) + 1
    # Sort by frequency
    sorted_freq = sorted(frequency.items(), key=lambda item: item[1], reverse=True)
    sorted_dict = {word: count for word, count in sorted_freq}
    return sorted_dict
     
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
        word_freq = word_frequency_analysis(epub_text)
        # For now, just show the extracted text (or you can process/store it as needed)
        return render_template('index.html', books=Book.query.order_by(Book.author.desc()).all(), word_freq=word_freq) 
    else:
        flash('Invalid file type')
        return redirect(request.url)