from flask.cli import FlaskGroup

from project import Word, WordBookLink, app, db, Book

cli = FlaskGroup(app)

@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command("seed_db")
def seed_db():
    db.session.add(Book(author="polaroid", title="the non-art of photos"))
    db.session.add(Book(author="kobo abe", title="woman in the dunes"))
    db.session.add(Word(word="the"))
    db.session.add(Word(word="non"))
    db.session.add(WordBookLink(wordid=1, bookid=1, frequency=10))
    db.session.add(WordBookLink(wordid=2, bookid=1, frequency=5))
    db.session.commit()

if __name__ == "__main__":
    cli()
