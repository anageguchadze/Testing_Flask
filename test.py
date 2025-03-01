import pytest 
from datetime import datetime
from app import app, db, Author, Book


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()


def test_author_book_relationship(client):
    with app.app_context():
        author = Author(name='J. K. Rowling', nationality='British')
        db.session.add(author)
        db.session.commit()

        book1 = Book(
            title="Harry Potter and the Philosopher's Stone",
            author=author,
            publication_date=datetime.strptime('1997, 6, 26', '%Y, %m, %d').date()
        )
        book2 = Book(
            title='Harry Potter and the Chamber of Secrets',
            author=author,
            publication_date=datetime.strptime('1998, 7, 2', '%Y, %m, %d').date()
        )

        db.session.add_all([book1, book2])
        db.session.commit()

        count = Book.query.filter_by(author=author).count()
        assert count == 2