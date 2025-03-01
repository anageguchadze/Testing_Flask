from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    nationality = db.Column(db.String(100), nullable=False)

    books = db.relationship('Book', backref='author', cascade='all, delete-orphan', lazy=True)



class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    publication_date = db.Column(db.Date, nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)

@app.route('/api/authors', methods=['GET'])
def list_authors():
    nationality = request.args.get('nationality')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    query = Author.query

    if nationality:
        query = query.filter_by(nationality=nationality)

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    authors = []

    for author in pagination.items:
        authors.append({
                'id': author.id,
                'name': author.name,
                'nationality': author.nationality
            })
        
    next_page = None
    if pagination.has_next:
        next_page = f'/api/authors/?page={pagination.next_num}&per_page={per_page}'

    return jsonify({'results': authors, 'next': next_page})


@app.route('/api/books', methods=['POST'])
def create_book():
    auth_header = request.headers.get('Authorization')
    if not auth_header or auth_header != 'Token secret':
        abort(401)

    data = request.get_json()
    title = data.get('title')
    publication_date_str = data.get('publication_date')

    if not title or not publication_date_str:
        return jsonify({'error': 'Missing fields'})
    try:
        publication_date = datetime.strptime(publication_date_str, '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Invalid date format'})
    
    book = Book(title=title, publication_date=publication_date)
    db.session.add(book)
    db.session.commit()

    return jsonify({
        'id': book.id,
        'title': book.title,
        'publication_date': book.publication_date.strftime('%Y-%m-%d')
    }), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)