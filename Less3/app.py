from os import abort
import sqlite3
from flask import Flask, request, jsonify, g
from pathlib import Path
from werkzeug.exceptions import HTTPException

#----------------------- ПОДКЛЮЧЕНИЕ К БД ---------------------
# знак / перегружен и работает как конкатенация
BASE_DIR = Path(__file__).parent
DATABASE = BASE_DIR / "quotes.db"  # <- тут путь к БД
# connection = sqlite3.connect(DATABASE)

#---------------- СОЗДАНИЕ ФЛАСК-ПРИЛОЖЕНИЯ -------------------
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

#--------- ФУНКЦИИ ДЛЯ ОПТИМИЗАЦИИ КОДА ПРИ РАБОТЕ С БД -------
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.errorhandler(HTTPException)
def handle_exception(e):
    return jsonify({"message": e.description}), e.code
#-------------------------------------------------------------


@app.get("/quotes")
def get_quotes():
    # Получение данных из БД
    select_quotes = "SELECT * FROM quotes"
    cursor = get_db().cursor()
    cursor.execute(select_quotes)
    quotes_db = cursor.fetchall() # get list[tuple]
    cursor.close()

    # Подготовка данных для возврата
    # Необходимо выполнить преобразование:
    # list[tuple] -> list[dict]
    keys = ["id", "rating", "author", "text"]
    quotes = []
    for quote_db in quotes_db:
        quote = dict(zip(keys, quote_db))
        quotes.append(quote)

    return jsonify(quotes) # list[dict] преобразуется в json


@app.get("/quotes/<int:quote_id>")
def get_quote_by_id(quote_id):
    # Получение данных из БД
    select_quote = f"SELECT * FROM quotes WHERE id=?"
    cursor = get_db().cursor()
    cursor.execute(select_quote, (quote_id,))
    quote = cursor.fetchone() # get tuple
    
    if quote:
        q = dict(zip(["id", "rating", "author", "text"], quote)) # dict
        return jsonify(q), 200

    return {"error": f"Quote with id={quote_id} not found"}, 404


@app.route("/quotes", methods=['POST'])
def create_quote():
    # Получение данных из БД
    new_data = request.json # get dict

    rating = new_data['rating']
    author = new_data['author']
    text = new_data['text']

    create_quote = f"INSERT INTO quotes (rating, author, text) VALUES (?, ?, ?);"
    cursor = get_db().cursor()
    cursor.execute(create_quote, (rating, author, text))
    cursor.connection.commit()
    last_id = cursor.lastrowid

    select_quote = f"SELECT * FROM quotes WHERE id=?"
    cursor.execute(select_quote, (last_id,))

    quote = cursor.fetchone() # get tuple
    
    if quote:
        q = dict(zip(["id", "rating", "author", "text"], quote)) # dict
        return jsonify(q), 201

    return {"error": f"Quote with id={last_id} was not created"}, 404


@app.route("/quotes/<int:quote_id>", methods=['PUT'])
def edit_quote(quote_id: int):

    keys = ["rating", "author", "text"]
    new_data = request.json

    cursor = get_db().cursor()
    for key in keys:
        if key in new_data:
            select_quote = f"UPDATE quotes SET {key} = ? WHERE id = ?;"
            cursor.execute(select_quote, (new_data[key], quote_id))
    cursor.connection.commit()

    select_quote = f"SELECT * FROM quotes WHERE id=?"
    cursor.execute(select_quote, (quote_id,))

    quote = cursor.fetchone() # get tuple
    
    if quote:
        q = dict(zip(["id", "rating", "author", "text"], quote)) # dict
        return jsonify(q), 200

    return {"error": f"Quote with id={quote_id} was not updated"}, 404


@app.route("/quotes/<int:quote_id>", methods=['DELETE'])
def delete(quote_id):
    cursor = get_db().cursor()
    select_quote = f"DELETE FROM quotes WHERE id = ?;"
    cursor.execute(select_quote, (quote_id,))
    cursor.connection.commit()
    
    return jsonify({"message": f"Quote with id {quote_id} has deleted."}), 200


if __name__ == "__main__":
    app.run(debug=True)