from flask import Flask, jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from pathlib import Path
from werkzeug.exceptions import HTTPException
from flask_migrate import Migrate

BASE_DIR = Path(__file__).parent

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{BASE_DIR / 'quotes.db'}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Для вывода содержимого SQL-запросов в консоли
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class AuthorModel(db.Model):
    __tablename__ = "authors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    surname = db.Column(db.String(32), server_default="", nullable=False)
    quotes = db.relationship('QuoteModel', backref='author', lazy='dynamic', cascade="all, delete-orphan")

    def __init__(self, name):
        self.name = name

    def __repr__(self) -> str:
        return f"Author: {self.name}, {self.surname}"
    

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname
            }        


class QuoteModel(db.Model):
    __tablename__ = "quotes"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), unique=False, nullable=False)
    rating = db.Column(db.Integer, server_default="1", default="1", nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey(AuthorModel.id), nullable=False)

    def __init__(self, author, text):
        self.author_id = author.id
        self.text  = text
    
    def __repr__(self) -> str:
        return f"Quote: {self.text}"
    
    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "author_id": self.author_id,
            "author_name": self.author.name, # backref='author'
            "author_surname": self.author.surname # backref='author'
        }


# Обработка ошибок и возврат значения в виде JSON
@app.errorhandler(HTTPException)
def handle_exception(e):
    return jsonify({"message": e.description}), e.code

#-----------------ValidationFunctions-------------------



#---------------------AuthorsModel----------------------

# GET AUTHORS (WITH Query parameter OrderBy = id, OrderBy = name)
@app.get("/authors")
def get_authors():
    """ Сериализация list[quotes] -> list[dict] -> str(JSON) """
    kwargs = request.args

    OrderBy = kwargs.get('OrderBy', 'id')
    Search = kwargs.get('Search', '')

    authors_db = AuthorModel.query.order_by(OrderBy).filter(or_(('~'+AuthorModel.name).contains(Search), AuthorModel.id.contains(Search))).all()
    authors = []
    if authors_db:
        for author_db in authors_db:
            authors.append(author_db.to_dict())
        return jsonify(authors), 200
    return jsonify([]), 200


# GET AUTHOR ORDER BY
@app.get("/authors/order_by/<parameter>") 
def get_author_order_by(parameter):
    authors_db = AuthorModel.query.order_by(parameter).all()

    authors = []
    if authors_db:
        for author_db in authors_db:
            authors.append(author_db.to_dict())
        return jsonify(authors), 200
    return jsonify([]), 200


# GET AUTHOR BY AUTHOR_ID
@app.get("/authors/<int:author_id>")
def get_author_by_id(author_id):
    author = AuthorModel.query.get(author_id) # .where id == author_id
    if author:
        return jsonify(author.to_dict()), 200
    abort(404, f"Author with id={author_id} not found")

# CREATE NEW AUTHOR
@app.post("/authors")
def create_new_author():

    # НУЖНА ПРОВЕРКА НА УНИКАЛЬНОСТЬ ИМЕНИ АВТОРА
    new_data = request.json # get dict

    author = AuthorModel(new_data.get('name'))

    if surname := new_data.get('surname'):
        author.surname = surname

    db.session.add(author)

    try:
        db.session.commit() # id присваивается объекту
        return jsonify(author.to_dict()), 201
    except:
        abort(400, f"NOT NULL constraint failed")

# EDIT AUTHOR BY AUTHOR_ID
@app.put("/authors/<int:author_id>")
def edit_author(author_id):
    author = AuthorModel.query.get(author_id)
    
    if author:
        # НУЖНА ПРОВЕРКА НА УНИКАЛЬНОСТЬ ИМЕНИ АВТОРА
        new_data = request.json # get dict
        setattr(author, 'name', new_data.get('name'))

        try:
            db.session.commit()
            return jsonify(author.to_dict()), 200
        except:
            abort(500) # если будет попытка сохранить дубликат по имени
    else:
        abort(404, f"Author with id={author_id} not found")

# DELETE AUTHOR BY AUTHOR_ID
# Заменить: вместо удаления в теле запроса менять статус поля deleted с 1 на 0
@app.delete("/authors/<int:author_id>")
def delete_author(author_id):
    author = AuthorModel.query.get(author_id)
    if author:
        db.session.delete(author)
        db.session.commit()
        return jsonify(message=f"Author with id={author_id} has deleted"), 200
    abort(404, f"Author with id={author_id} not found")


# # GET DELETED AUTHORS
# @app.get("/authors/deleted")


# # RESTORE DELETED AUTHORS
# @app.post("/authors/restore/<int:deleted_author_id>")


#---------------------QuotesModel----------------------

# GET ALL QUOTES
@app.get("/quotes")
def get_quotes():
    """ Сериализация list[quotes] -> list[dict] -> str(JSON) """
    quotes_db = QuoteModel.query.all()
    quotes = []
    for quote_db in quotes_db:
        quotes.append(quote_db.to_dict())
    return jsonify(quotes), 200

# GET QUOTE BY QUOTE_ID
@app.get("/quotes/<int:quote_id>")
def get_quote_id(quote_id):
    quote = QuoteModel.query.get(quote_id)
    if quote:
        return jsonify(quote.to_dict()), 200
    abort(404, f"Quote with id={quote_id} not found")
    #return {"error": f"Quote with id={quote_id} not found"}, 404

# GET RATING UP  # POST ЛЮБЫЕ ИЗМЕНЕНИЯ!!!
@app.post("/quotes/<int:quote_id>/up")
def get_rating_up(quote_id):
    quote = QuoteModel.query.get(quote_id)

    if quote:
        if quote.rating < 5:
            quote.rating += 1
        else:
            quote.rating = 5
        try:
            db.session.commit()
            return jsonify(quote.to_dict()), 200
        except:
            abort(500)
    abort(404, f"Quote with id={quote_id} not found")


# GET RATING DOWN
@app.post("/quotes/<int:quote_id>/down")
def get_rating_down(quote_id):
    quote = QuoteModel.query.get(quote_id)
    
    if quote:
        if quote.rating > 1:
            quote.rating -= 1
        else:
            quote.rating = 1
        try:
            db.session.commit()
            return jsonify(quote.to_dict()), 200
        except:
            abort(500)
    abort(404, f"Quote with id={quote_id} not found")
   

# GET QUOTES BY AUTHOR_ID
@app.get("/authors/<int:author_id>/quotes")
def get_quotes_by_author_id(author_id):

    # author_id_quotes = QuoteModel.query.filter_by(author_id = author_id).all()
    author_id_quotes = QuoteModel.query.join(AuthorModel, AuthorModel.id == QuoteModel.author_id).filter(QuoteModel.author_id == author_id).all()

    # author_id_quotes = db.session.query(QuoteModel, AuthorModel.name, AuthorModel.surname).join(AuthorModel).filter(QuoteModel.author_id == author_id).all()
    # print(type(author_id_quotes))

    if author_id_quotes:
        quotes = []
        for a_id_quote in author_id_quotes:
            quotes.append(a_id_quote.to_dict())
        return jsonify(quotes), 200
    return jsonify([]), 200

    #         quotes.append( \
    #         {
    #             "author_id": a_id_quote.quotes_author_id,
    #             "author_name": a_id_quote.author_name,
    #         })
    # "author_id": 5,
    # "author_name": "Clint",
    # "author_surname": "Eastwood",
    # "id": 12,
    # "rating": 1,
    # "text": "Quote by default"


# CREATE QUOTE BY AUTHOR_ID
@app.post("/authors/<int:author_id>/quotes")
def create_quote_by_author_id(author_id):
    author = AuthorModel.query.get(author_id)
    data = request.json
    new_quote = QuoteModel(author, data.get("text", "Quote by default"))
    
    if rating := data.get('rating'):
        if rating in range(1,5+1):
            new_quote.rating = rating
        elif rating < 1:
            new_quote.rating = 1
        elif rating > 5:
            new_quote.rating = 5

    db.session.add(new_quote)
    db.session.commit()
    return new_quote.to_dict(), 201


# EDIT QUOTE BY QUOTE_ID
@app.put("/quotes/<int:quote_id>")
def edit_quote(quote_id):
    quote = QuoteModel.query.get(quote_id)
    if quote:
        new_data = request.json # get dict

        # Частный подход
        # if text := new_data.get('text'):
        #     quote.text = text
        
        # Универсальный подход
        for key, value in new_data.items():
            setattr(quote, key, value) # вспоминаем Python уровень 2
        try:
            db.session.commit()
            return jsonify(quote.to_dict()), 200
        except:
            abort(500)
    else:
        abort(404, f"Quote with id={quote_id} not found")

# DELETE QUOTE BY QUOTE_ID
@app.delete("/quotes/<int:quote_id>")
def delete_quote(quote_id):
    quote = QuoteModel.query.get(quote_id)
    if quote:
        db.session.delete(quote)
        db.session.commit()
        return jsonify(message=f"Quote with id={quote_id} has deleted"), 200
    abort(404, f"Quote with id={quote_id} not found")


if __name__ == "__main__":
    app.run(debug=True)

