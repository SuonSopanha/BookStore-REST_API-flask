from models import *

def seed_books():
    # Seed data for books
    books_data = [
        {
            'isbn': '1234567890123',
            'title': 'Bleach',
            'author': 'Tite Kubo',
            'genre': 'Fiction',
            'price': 29.99,
            'quantity_available': 100,
        },
        {
            'isbn': '9876543210987',
            'title': 'The Road',
            'author': 'Jane Smith',
            'genre': 'Philosophy',
            'price': 19.99,
            'quantity_available': 50,
        },

        {
            'isbn': '4567890123456',
            'title': 'Harry Potter and the Philosopher\'s Stone',
            'author': 'J.K. Rowling',
            'genre': 'Fantasy',
            'price': 9.99,
            'quantity_available': 200,
        }
        # Add more book entries as needed
    ]

    # Insert seed data into the database
    for book_data in books_data:
        book = Book(**book_data)
        db.session.add(book)

    # Commit the changes
    db.session.commit()