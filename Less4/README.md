## ipython

Это улучшенный интерпретатор с возможностями id,
(улучшенный интерактивный питон)
```
ipython
// команда для запуска
```

Здесь есть подсказки:
* 'hello'.  и ipython подсвечивает методы, которые можно применить к строке
* есть история команд

работа ведется в ячейках:
```
In[1]: - входная ячейка
Out[1]: - выходная ячейка
```

## создание БД
```
In[3]:  from app import app, db, QuoteModel
In[4]: app.app_context().push()
In[5]: db.create_all()
// после этого мы увидим, что была создана main.db
```

## создание записи
```
In[6]:q1 = QuoteModel('Народная мудрость', 'Нет пламя без огня')
// создаем экземпляр на основе класса
In[6]:q1.author
Out[6]: 'Народная мудрость'
In[7]:q1.text
Out[7]: 'Нет пламя без огня'

In[8]: db.session.add(q1)
// добавление записи в БД

In[9]: db.session.commit()
// делаем комит, чтобы подтвердить изменения

In[10]:q1.id
Out[10]: 1
// Запись добавлена, у q1 появился id!
```

## дорабатываем класс для корректной работы приложения
```
In[11]:QuoteModel.query.all()
Out[11]: [<QuoteModel 1>]
// через класс получили все записи
```
Чтобы записи хорошо отображались необходимо в класс QuoteModel
добавить __repr__() -> добавляем эту ф-ю в наш класс и
перезагружаем ipython
```
In [1]: from app import app, db, QuoteModel
In [2]: app.app_context().push()
In [3]: QuoteModel.query.all()
Out[3]: [Quote: 1, Народная мудрость, Нет пламя без огня]
```
Все получилось.
Теперь необходимо переписать все наши методы для работы с ORM

Что вернулось при исполнении команды: QuoteModel.query.all() ?
Список экземпляров. А значит нам этот список экземпляров нужно
преобразовать в список словарей (который впоследствии станет JSON-ом).
Для этой цели создадим специальный метод def to_dict(self)

После этого шага можем описать функцию def get_quote() Готово.

Реализуем остальные контроллеры:
- get quote by id
- create quote
- edit quote
- delete quote

Запускаем python3 app.py и проверяем работу приложения
