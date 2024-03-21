
## Установка пакетов из Less5: pip install -r requirements.txt

## Связи в моделях
- One-to-One (строго один автор - одна цитата)
- One-to-Many (у одного автора может быть много цитат) *
- Many-to-Many (у авторов много цитат, и у цитаты мб несколько авторов)

## Параметры связей
```backref``` -  простой способ создать обратную связь для  AuthorModel. Вы можете также использовать author.quotes чтобы обратиться к цитатам данного автора.
```lazy``` определяет, когда SQLAlchemy будет загружать данные из базы данных:
●	'select' (значение по умолчанию) означет что SQLAlchemy будет загружать данные по мере необходимости в один заход с использованием стандартного оператора выбора.
●	'joined' говорит SQLAlchemy загружать связи в том же запросе что и родительский используя оператор JOIN.
●	'subquery' работает как 'joined', но SQLAlchemy использует подзапрос.
●	'dynamic' является особенно полезным, если у вас есть много элементов. Вместо того чтобы загружать элементы SQLAlchemy будет возвращать объект запроса, который вы можете дополнительно уточнить перед загрузкой элементов. Как правило, это как раз то, в чем вы нуждаетесь, если ожидаете более чем несколько элементов для этих связей.
```cascade="all, delete-orphan"``` - организация каскадного удаления
(когда мы удаляем автора, то удаляются и все его цитаты)

## Заново пересоздаем БД, т.к. мы существенно изменили модель QuoteModel
// author_id = db.Column(db.Integer, db.ForeignKey(AuthorModel.id))

В рабочей ситуации нужно было бы выгрузить данные из таблицы,
создать новую таблицу и загрузить туда наши данные в соответствующие поля

## Удаляем БД и миграцию
```
main.db
590454baad92_0001_initial_migrations
```
зачищаем папку versions/__pycache__ (в которой еще остаются удаленные ранее миграции)

## Создаем миграцию и делаем апгрейд
```
flask db migrate -m "0001_initial_migrations"
flask db upgrade
```
// Получаем БД уже с двумя таблицами, в соответствии с нашими моделями

## Используя flask-shell-ipython добавляем записи в нашу БД
```
pip install flask-shell-ipython # установка ipython в качестве интерпретатора для flask shell
flask shell # запуск ipython в контексте flask-приложения
```
// Благодаря этому, у нас весь контекст загрузился автоматически, таким образом
нет необходимости импортировать каждый раз: app, db, QuoteModel, AuthorModel
как это было необходимо было делать в ipython

## Создаем автора 'Tom'
```
In [2]: author1 = AuthorModel('Tom')
In [3]: db.session.add(author1)
In [4]: db.session.commit()
In [5]: author1
Out[5]: Author: Tom
In [6]: author1.id
Out[6]: 1
```
## Cоздаем цитату
```
In [7]: q1 = QuoteModel(author1, 'Первая цитата Тома')
In [8]: db.session.add(q1)
In [9]: db.session.commit()
In [10]: q1
Out[10]: Quote: Первая цитата Тома
In [11]: q1.id
Out[11]: 1
```
## Создаем коллекции QuotesAPI_Authors и QuotesAPI_Quotes

## Реализуем все методы для моделей AuthorModel и QuoteModel

## Решение возможных проблем при создании миграций в SQLite:

- [Flask-Migrate DOCS](https://flask-migrate.readthedocs.io/en/latest/)
- [Fixing ALTER TABLE errors with Flask-Migrate and SQLite](https://blog.miguelgrinberg.com/post/fixing-alter-table-errors-with-flask-migrate-and-sqlite)
- [Как реализовать действия неподдерживаемых операторов команды ALTER TABLE в SQLite3](https://webhamster.ru/mytetrashare/index/mtb0/1356422142eucsluo0cv)

## Полезные ссылки по SQLAlchemy:

- [Flask-SQLAlchemy Быстрый старт (RUS)](https://flask-sqlalchemy-russian.readthedocs.io/ru/latest/quickstart.html#id3)
- [Flask-SQLAlchemy Декларирование моделей (RUS)](https://flask-sqlalchemy-russian.readthedocs.io/ru/latest/models.html#models)
- [SQLAlchemy Object Relational Tutorial (1.x API) (ENG)](https://docs.sqlalchemy.org/en/14/orm/tutorial.html#building-a-relationship)


## Добавляем Автору свойство surname
```
surname = db.Column(db.String(32), server_default="", nullable=False)
```
## Создаем миграцию и накатываем БД
```
bash:
flask db migrate -m "0002_add surname"
flask db upgrade
```

## Добавляем больше функционала (дополнительные задания)

1.	Добавьте цитатам рейтинги - целое значение от 1 до 5.
a.	Запретите хранить в поле пустое(NULL) значение, для этого в классе модели для колонки пропишите: nullable=False
b.	Вам пригодятся параметры: 
default - задает значение по умолчанию, устанавливается при создании нового объекта
server_default - задает значение по умолчанию для новых полей существующих объектов в БД. Работает при создании миграций.
c.	При создании цитаты без указания рейтинга, рейтинг по умолчанию устанавливается 1
d.	Если рейтинг указан, то задается тот, что указан в теле POST-запроса. Но в диапазоне 1...5.
2.	Добавьте url’ы позволяющий увеличивать рейтинг цитаты на +1 и уменьшать -1
Подумайте, как данные url’ы должны выглядеть.
Детали реализации:
a.	Если отправляем запрос на +1 к рейтингу, а рейтинг максимальной, то рейтинг остается максимальным(не изменяетися), 
сервер отвечает 200 OK
b.	Тоже с попыткой уменьшить, при самом низком рейтинге

3.	У вас уже должно быть реализовано получение списка авторов.
Добавьте возможность задавать сортировку по:
a.	Имени автора и/или по фамилии
b.	Если у автора нет фамилии, добавьте
	Как реализовать фильтр:
- [russianblogs !!!](https://russianblogs.com/article/398988656/)
- [riptutorial.com](https://riptutorial.com/sqlalchemy/example/6615/filtering)
- [flask-sqlalchemy.palletsprojects.com](https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/#querying-records)
4.	Проверьте, что при удалении пользователя, удаляются и все его цитаты.
Как это правильно сделать:
- [docs.sqlalchemy.org](https://docs.sqlalchemy.org/en/14/orm/cascades.html)
- [digitrain.ru](https://digitrain.ru/questions/23323947/)
5.	На практике, при удалении информации, она(информация) крайне редко удаляется из базы, а чаще помечается как “удаленная”.
Вместо удаления пользователя, добавьте ему пометку “Удален”. 
Удаленные пользователи и их цитаты не должны отображаться в ответах сервера.
Должен быть url для запроса всех удаленных пользователей и url их восстановления.
6.	Добавьте для Цитаты дату создания, дата должна устанавливать значение автоматически, при создании новой цитаты. Отображайте дату в JSON-ответе в формате: “dd.mm.yyyy”
Подсказка:
Для добавления свойства “дата создания” используйте:
created = db.Column(db.DateTime(timezone=True), server_default=func.now())

## Добавляем Цитате свойство rating
```
rating = db.Column(db.Integer, server_default="1", default="1", nullable=False)
```
## Создаем миграцию и накатываем БД
```
bash:
flask db migrate -m "0003_add rating"
flask db upgrade
```
## Из доп заданий выполнил 1-4...не доделал 5, 6
