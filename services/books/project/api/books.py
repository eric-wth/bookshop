from sqlalchemy import exc

from flask import Blueprint, jsonify, request, render_template

from project.api.models import Book
from project import db


books_blueprint = Blueprint('books', __name__)

@books_blueprint.route('/users/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


# Create a book
@books_blueprint.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    new_book = Book(
        title=data['title'],
        author_id=data['author_id'],
        description=data['description'],
        price=data['price'],
        cover_image_url=data.get('cover_image_url'),
        file_url=data.get('file_url'),
        published_at=data['published_at'],
        category_id=data['category_id']
    )
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'message': 'Book created', 'id': new_book.id}), 201


# Read all books
@books_blueprint.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([{
        'id': book.id,
        'title': book.title,
        'author_id': book.author_id,
        'description': book.description,
        'price': book.price,
        'cover_image_url': book.cover_image_url,
        'file_url': book.file_url,
        'published_at': book.published_at,
        'category_id': book.category_id,
        'created_at': book.created_at,
        'updated_at': book.updated_at
    } for book in books]), 200


# Read a specific book
@books_blueprint.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    return jsonify({
        'id': book.id,
        'title': book.title,
        'author_id': book.author_id,
        'description': book.description,
        'price': book.price,
        'cover_image_url': book.cover_image_url,
        'file_url': book.file_url,
        'published_at': book.published_at,
        'category_id': book.category_id,
        'created_at': book.created_at,
        'updated_at': book.updated_at
    }), 200


# Update a book
@books_blueprint.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    data = request.get_json()

    book.title = data.get('title', book.title)
    book.author_id = data.get('author_id', book.author_id)
    book.description = data.get('description', book.description)
    book.price = data.get('price', book.price)
    book.cover_image_url = data.get('cover_image_url', book.cover_image_url)
    book.file_url = data.get('file_url', book.file_url)
    book.published_at = data.get('published_at', book.published_at)
    book.category_id = data.get('category_id', book.category_id)

    db.session.commit()
    return jsonify({'message': 'Book updated'}), 200


# Delete a book
@books_blueprint.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted'}), 200