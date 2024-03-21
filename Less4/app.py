from flask import Flask, jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
from werkzeug.exceptions import HTTPException

BASE_DIR = Path(__file__).parent

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{BASE_DIR / 'main.db'}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class QuoteModel(db.Model): # как наследование происходит здесь ?
    __tablename__ = "quotes"
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(32), unique=False)
    text = db.Column(db.String(255), unique=False)


    def __init__(self, author, text):
        self.author = author
        self.text  = text
        
    
    def __repr__(self) -> str:
        return f"Quote: {self.id}, {self.author}, {self.text}"
    
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
    return {"error": f"Quote with id={quote_id} not found"}, 404


@app.post("/quotes")
def create_new_quote():
    new_data = request.json # get dict
    
    a = new_data['author']
    t = new_data['text']

    q = QuoteModel(author = a, text = t)
    db.session.add(q)
    db.session.commit()

    quote = QuoteModel.query.get(q.id)
    return jsonify(quote.to_dict()), 200


@app.put("/quotes/<int:quote_id>")
def edit_quote(quote_id):
    q = QuoteModel.query.get(quote_id)
    if q:
        new_data = request.json # get dict
        q.text = new_data['text'] if 'text' in new_data else q.text
        q.author = new_data['author'] if 'author' in new_data else q.author
        db.session.commit()

        return jsonify(q.to_dict()), 200
    return {"error": f"Quote with id={quote_id} not found"}, 404


@app.delete("/quotes/<int:quote_id>")
def delete_quote(quote_id):
    q = QuoteModel.query.get(quote_id)
    if q:
        db.session.delete(q)
        db.session.commit()
        return {"message": f"Quote with id={quote_id} has deleted"}, 200
    return {"error": f"Quote with id={quote_id} not found"}, 404


@app.get("/quotes/filter")
def get_quote_by_filter():
    pass

if __name__ == "__main__":
    app.run(debug=True)
    init_rating()