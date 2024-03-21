from flask import Flask, jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
from werkzeug.exceptions import HTTPException
from flask_migrate import Migrate # Less5

BASE_DIR = Path(__file__).parent

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{BASE_DIR / 'main.db'}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Для вывода содержимого SQL-запросов в консоли
# app.config['SQLALCHEMY_ECHO'] = True # Less5 (ридми)

db = SQLAlchemy(app)
migrate = Migrate(app, db) # Less5

class QuoteModel(db.Model): # как наследование происходит здесь ?
    __tablename__ = "quotes"
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(32), unique=False, nullable=False)
    text = db.Column(db.String(255), unique=False, nullable=False)


    def __init__(self, author, text):
        self.author = author
        self.text  = text
        
    
    def __repr__(self) -> str:
        return f"Quote: {self.id}, {self.author}, {self.text}"
    
    @staticmethod
    def validate(in_data):
        """ Валидация на случай если ключи неправильные передаются
        Если множества равны, то вернется True"""
        return set(in_data.keys()) == set(("author", "text"))


    def to_dict(self):
        return {
            "id": self.id,
            "author": self.author,
            "text": self.text
            }

# Обработка ошибок и возврат значения в виде JSON
@app.errorhandler(HTTPException)
def handle_exception(e):
    return jsonify({"message": e.description}), e.code

# ---------------------------------------------------------- #
# ipython используем только для тестирования sqlachemy в консоли,
# добавлять его в requirements.txt не нужно!

@app.route("/quotes")
def get_quotes():
    """ Сериализация list[quotes] -> list[dict] -> str(JSON) """
    quotes_db = QuoteModel.query.all()
    quotes = []
    for quote_db in quotes_db:
        quotes.append(quote_db.to_dict())
    return jsonify(quotes), 200

@app.get("/quotes/<int:quote_id>")
def get_quote_id(quote_id):
    quote = QuoteModel.query.get(quote_id)
    if quote:
        return jsonify(quote.to_dict()), 200
    abort(404, f"Quote with id={quote_id} not found")
    #return {"error": f"Quote with id={quote_id} not found"}, 404

@app.post("/quotes")
def create_new_quote():
    new_data = request.json # get dict
    if QuoteModel.validate(new_data):

        q = QuoteModel(**new_data)
        db.session.add(q)
        try:
            db.session.commit()
            return jsonify(q.to_dict()), 200
        except:
            abort(400, f"NOT NULL constraint failed")
    else:
        abort(400, f"Bad data")

@app.put("/quotes/<int:quote_id>")
def edit_quote(quote_id):
    q = QuoteModel.query.get(quote_id)
    if q:
        new_data = request.json # get dict

        # Частный подход
        # if text := new_data.get('text'):
        #     q.text = text
        # if author := new_data.get('author'):
        #     q.author = author
        
        # Универсальный подход
        for key, value in new_data.items():
            setattr(q, key, value) # вспоминаем Python уровень 2
        try:
            db.session.commit()
            return jsonify(q.to_dict()), 200
        except:
            abort(500) # в каком случае это отработает???
    else:
        abort(404, f"Quote with id={quote_id} not found")

@app.delete("/quotes/<int:quote_id>")
def delete_quote(quote_id):
    q = QuoteModel.query.get(quote_id)
    if q:
        db.session.delete(q)
        db.session.commit()
        return jsonify(message=f"Quote with id={quote_id} has deleted"), 200
    abort(404, f"Quote with id={quote_id} not found")


@app.get("/quotes/filter")
def get_quotes_by_filter():
    """ Сериализация list[quotes] -> list[dict] -> str(JSON) """
    kwargs = request.args # kwargs = ImmutableMultiDict([('author', 'Tom')])
    filtered_quotes = QuoteModel.query.filter_by(**kwargs).all()

    if filtered_quotes:
        quotes = []
        for f_q in filtered_quotes:
            quotes.append(f_q.to_dict())
        return jsonify(quotes), 200
    return jsonify([]), 200 # возвращаем пустой список если ничего не нашли

if __name__ == "__main__":
    app.run(debug=True)
