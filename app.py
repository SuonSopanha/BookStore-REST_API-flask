from flask import Flask, request, json
from flask_restx import Api, Resource, fields, reqparse
from config import Config
from models import db, Book
config = Config()

app = Flask(__name__)



api = Api(app)
api_ns = api.namespace("api", path='/' , description="API")

app.config.from_object(config)


db.init_app(app)

with app.app_context():
    db.create_all()
    from seed import seed_books
    #check if table in empty
    if Book.query.count() == 0:
        seed_books()
    

book_model = api.model('BookOutput', {
    'id': fields.Integer,
    'isbn': fields.String,
    'title': fields.String,
    'author': fields.String,
    'genre': fields.String,
    'price': fields.Float,
    'quantity_available': fields.Integer,
})

book_parser = reqparse.RequestParser()
book_parser.add_argument('isbn', required=True)
book_parser.add_argument('title', required=True)
book_parser.add_argument('author', required=True)
book_parser.add_argument('genre', required=True)
book_parser.add_argument('price', required=True)
book_parser.add_argument('quantity_available', required=True)


@api_ns.route('/Book')
class Books(Resource):
    @api_ns.marshal_with(book_model, as_list=True)
    def get(self):
        books = Book.query.all()
        return books
    
    @api_ns.expect(book_model)
    @api_ns.marshal_with(book_model)
    def post(self):
        args = book_parser.parse_args()
        book = Book(**args)
        db.session.add(book)
        db.session.commit()
        return book
    
@api_ns.route('/Book/<id>')
class BookById(Resource):
    @api_ns.marshal_with(book_model)
    def get(self, id):
        book = Book.query.filter_by(id=id).first()
        return book
    

    @api_ns.expect(book_model)
    @api_ns.marshal_with(book_model)
    def put(self, id):
        book = Book.query.get_or_404(id)
        args = book_parser.parse_args()
        for key, value in args.items():
            setattr(book, key, value)
        db.session.commit()
        return book
    

    @api_ns.marshal_with(book_model)
    def delete(self, id):
        book = Book.query.filter_by(id=id).first()
        db.session.delete(book)
        db.session.commit()
        return book


@api_ns.route('/Book/author/<author>')
class BooksByAuthor(Resource):
    @api_ns.marshal_with(book_model, as_list=True)
    def get(self, author):
        books = Book.query.filter_by(author=author).all()
        return books


@api_ns.route('/Book/isbn/<int:isbn>')
class BookByISBN(Resource):
    @api_ns.marshal_with(book_model)
    def get(self, isbn):
        book = Book.query.filter_by(isbn=isbn).first()
        return book
    

@api_ns.route('/Book/genre/<genre>')
class BooksByGenre(Resource):
    @api_ns.marshal_with(book_model, as_list=True)
    def get(self, genre):
        books = Book.query.filter_by(genre=genre).all()
        return books
    





if __name__=='__main__':
    app.run()