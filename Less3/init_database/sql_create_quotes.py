import sqlite3

# В конце каждой конструкции на SQL важно ставить ;
create_quotes = """
    INSERT INTO
    quotes (rating,author,text)
    VALUES
    (1, 'Rick Cook', 'Программирование сегодня — это гонка разработчиков программ...'),
    (1, 'Waldi Ravens', 'Программирование на С похоже на быстрые танцы на только...'),
    (1, 'Mosher’s Law of Software Engineering', 'Не волнуйтесь, если что-то не работает. Если бы всё работало, вас бы уволили.'),
    (1, 'Yoggi Berra', 'В теории, теория и практика неразделимы. На практике это не так.');
    """

# Подключение в БД
connection = sqlite3.connect("test.db")

# Создаем cursor, он позволяет делать SQL-запросы
cursor = connection.cursor()

# Выполняем запрос:
cursor.execute(create_quotes)

# Фиксируем выполнение(транзакцию)
connection.commit()

# Закрыть курсор:
cursor.close()

# Закрыть соединение:
connection.close()
