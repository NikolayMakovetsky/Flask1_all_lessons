from random import choice
from flask import Flask, request, jsonify
from collections import Counter

app = Flask(__name__)
# Чтобы исправить проблему с юникод последовательностями добавляем строку с настройкой:
# Обновляем страницу в браузере, радуемся :-)
app.config['JSON_AS_ASCII'] = False


about_me = {
   "name": "Иосиф",
   "surname": "Цыпленков",
   "email": "tcyplenkov@mail.ru"
}

quotes = [
   {
       "id": 3,
       "author": "Rick Cook",
       "text": "Программирование сегодня — это гонка разработчиков программ, стремящихся писать программы с большей и лучшей идиотоустойчивостью, и вселенной, которая пытается создать больше отборных идиотов. Пока вселенная побеждает."
   },
   {
       "id": 5,
       "author": "Waldi Ravens",
       "text": "Программирование на С похоже на быстрые танцы на только что отполированном полу людей с острыми бритвами в руках."
   },
   {
       "id": 6,
       "author": "Mosher’s Law of Software Engineering",
       "text": "Не волнуйтесь, если что-то не работает. Если бы всё работало, вас бы уволили."
   },
   {
       "id": 8,
       "author": "Yoggi Berra",
       "text": "В теории, теория и практика неразделимы. На практике это не так."
   },

]


@app.route("/")
def hello_world():
    return "Hello, World! lesson 2"


@app.route("/about")
def about():
    return about_me


# /quotes
@app.route("/quotes")
def get_quotes():
    return quotes


# /quotes/3
# /quotes/5
# /quotes/6
# /quotes/8
@app.route("/quotes/<int:quote_id>")
def get_quote_by_id(quote_id):
    """ Function returns the quote by id. 
        Type of the quote is dict -> json str """
    for quote in quotes:
        if quote["id"] == quote_id:
            # dict -> json str
            return quote, 200
        
    return {"error": f"Quote with id={quote_id} not found"}, 404


# dict -> json str
@app.route("/quotes/count")
def quotes_count():
    return {"count": len(quotes)}, 200


# dict -> json str
@app.route("/quotes/random", methods=['GET'])
def random_quote():
    return choice(quotes), 200

def new_quote_id():
    return quotes[-1]["id"] + 1

@app.route("/quotes", methods=['POST'])
def create_quote():
    data = request.json  # json -> dict (десериализация происходит)
    print("data = ", data, type(data)) # после запуска смотри командную строку
    data["id"] = new_quote_id()
    if "rating" not in data or data["rating"] not in range(1, 6):
        data["rating"] = 1
    quotes.append(data)
    return jsonify(data), 201


@app.route("/quotes/<int:quote_id>", methods=['PUT'])
def edit_quote(quote_id: int):
    new_data = request.json

    for quote in quotes:
        # print(quote["id"], type(quote["id"]), quote_id, type(quote_id))
        if quote["id"] == quote_id:
            quote.update(new_data)
            return jsonify(quote), 200
    
    return {"error": f"Quote with id={quote_id} not found"}, 404

@app.route("/quotes/<int:quote_id>", methods=['DELETE'])
def delete(quote_id):
    # delete quote with id
    for quote in quotes:
        if quote["id"] == quote_id:
            quotes.remove(quote)
            return jsonify({"message": f"Quote with id {quote_id} has deleted."}), 200
    
    return {"error": f"Quote with id={quote_id} not found"}, 404

# ------------------ HOMEWORK ---------------------

#/quotes/filter?author=Alex - найдет все цитаты с автором Alex
#/quotes/filter?author=Ivan&rating=5 - найти все цитаты Ивана с рейтингом 5

def add_kv_to_dict(dct: dict, key: str, val=None):
    """Добавляет в передаваемый словарь парy ключ: значение"""
    if key not in dct:
        dct[key] = val

@app.route('/quotes/filter', methods=['GET'])
def ger_quote_by_filter():

    for quote in quotes: # добавляем поле 'рейтинг' в исх.словарь для исключ ошибок
        add_kv_to_dict(quote, 'rating', val=1)
    
    args = request.args
    fp = {
    'author' : args.get('author'),  # str
    'id' : args.get('id'),          # str (int)
    'rating' : args.get('rating')   # str (int)
    }

    quote_ids = {}
    if fp['author'] is not None:
        quote_ids[fp['author']] = [i for i,d in enumerate(quotes) if d['author'] == fp['author']]
    if fp['id'] is not None:
        if '-' in fp['id']:
            start, stop = map(int, fp['id'].split('-'))
            quote_ids[fp['id']] = [i for i,d in enumerate(quotes) if d['id'] in range(start,stop)]
        else:
            quote_ids[fp['id']] = [i for i,d in enumerate(quotes) if d['id'] == int(fp['id'])]
    if fp['rating'] is not None:
        quote_ids[fp['rating']] = [i for i,d in enumerate(quotes) if d['rating'] == int(fp['rating'])]
    
    c = Counter(sum(quote_ids.values(), []))
    quote_filter = [k for k,v in c.items() if v == len(quote_ids)]

    if quote_filter:
        return jsonify([quotes[i] for i in quote_filter]), 200
    return {"error": f"Quote with filter:{fp} not found"}, 404


if __name__ == "__main__":
    app.run(debug=True)