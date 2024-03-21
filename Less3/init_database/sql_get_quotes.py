import sqlite3

select_quotes = "SELECT * from quotes"

# Подключение в БД
# Создаем cursor, он позволяет делать SQL-запросы
connection = sqlite3.connect("test.db")
cursor = connection.cursor()

# Выполняем запрос:
cursor.execute(select_quotes)

# Извлекаем результаты запроса
# fetchone() выберет первую запись
# fetchall() возвращает список кортежей
quotes = cursor.fetchall()
print(f"{quotes=}")

# Закрыть курсор:
# Закрыть соединение:
cursor.close()
connection.close()
