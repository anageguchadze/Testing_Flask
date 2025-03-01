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

        db.session.delete(author)
        db.session.commit()

        total_books = Book.query.count()
        assert total_books == 0

def test_book_creation(client):
    response = client.post(
        '/api/books',
        json={
            'title': 'Harry Potter and the prisoner of Azkaban',
            'publication_date': '1999-07-08' 
        }
    )
    assert response.status_code == 401

def test_author_pagination(client):
    with app.app_context():
        for i in range(5):
            author = Author(name=f'Author {i}', nationality=f'Country {i}')
            db.session.add(author)
        db.session.commit()

        response = client.get('/api/authors?per_page=5')
        data = response.get_json()
        assert response.status_code == 200
        assert len(data['results']) == 5
        assert 'next' in data
        assert data['next'] is None