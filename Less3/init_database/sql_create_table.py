import sqlite3

create_table = """
CREATE TABLE IF NOT EXISTS quotes (
id INTEGER PRIMARY KEY AUTOINCREMENT,
rating INTEGER NOT NULL,
author TEXT NOT NULL,
text TEXT NOT NULL
);
"""
# Подключение в БД (создаем соединение)
# Указываем абс или *относ путь
# экземпляр класса Сonnection
connection = sqlite3.connect("test.db")

# Создаем cursor, он позволяет делать SQL-запросы
# экземпляр класса Сursor
cursor = connection.cursor()

# Выполняем запрос:
cursor.execute(create_table)

# Фиксируем выполнение(транзакцию)
# Комит - подтверждение изменений
# ВАЖНО! КОМИТ МЫ ВЫЗЫВАЕМ ИМЕННО У КОНЕКШ
connection.commit()

# Закрыть курсор:
# При закрытии соединения курсор по умолчанию будет закрыт,
# но для порядка в коде мы его закрываем явно
cursor.close()

# Закрыть соединение:
connection.close()

