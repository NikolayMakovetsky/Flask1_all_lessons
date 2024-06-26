
## Миграции
Миграция - переход от одной структуры БД к другой без потери консистентности.
Миграции - что-то вроде системы контроля версий для вашей базы данных.
Они позволяют вашей команде изменять структуру БД, в то же время оставаясь в курсе изменений других участников.

Миграции бывают:
- Апгрейд (переход в новое состояние)
- Даунгрейд (возврат к предыдущему состоянию)

Список изменений состояния БД и есть список миграций!

Для работы с миграциями нужно установить специальный пакет
pip install flask-migrate

## Подготовка к созданию БД
(т.к. при работе с миграциями БД создается с нуля)
// файл quotes.sql содержит информацию для БД, выгруженную из Less4

Добавляем строчки кода в наш app.py
```
from flask_migrate import Migrate # Less5
migrate = Migrate(app, db) # Less5
```
Важно! Под капотом класс Migrate использует библиотеку Alembic,
которая выполняет всю низкоуровненую работу и занимается кодогенерацией

## I) Инициализация БД
В консоли набираем команду
flask db init
// произошло создание шаблона для того, чтобы хранить наши миграции
// создалась директория migrations

файл script.py.mako в директории migrations
содержит следующие строчки:

```
def upgrade():
    ${upgrades if upgrades else "pass"}


def downgrade():
    ${downgrades if downgrades else "pass"}
```

upgrade - используется чтобы 'накатить' изменения
downgrade - чтобы 'откатить' изменения

Для чего может понадобиться откат изменений?
В самых сложных случаях, когда для того, чтобы накатить, 
нужно для начала откатить БД до одной из предыдущих миграций!

## II) Создание миграции
Делается при каждом изменении модели БД (QuoteModel)
flask db migrate -m "Initial migrations"

1. появился файл main.db
// при этом в самой бд пока есть только пустая служебная таблица alembic_version

2. в папке versions появился файл 74602cd88f5f_initial_migrations.py
def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('quotes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('author', sa.String(length=32), nullable=True),
    sa.Column('text', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('quotes')
    # ### end Alembic commands ###

## III) Накатывание БД
flask db upgrade

В нашей бд появилась таблица quotes, а в служебной таблицe
alembic_version номер миграции, которую мы накатили

## ------
В более сложных проектах вместо app.py создают отдельные файлы:
- Модель
- Настройки
- Вьюшки и т.д.
(В джанго в рамках одного проекта есть приложение ViewPrint)

## Переименовывание миграции
flask db downgrade
После этого находим файл 74602cd88f5f_initial_migrations.py
и вручную его переименовываем, добавляя номер для удобства
74602cd88f5f_0001_initial_migrations.py

## app.config['SQLALCHEMY_ECHO'] = True
Добавление этой строки дает возможность увидеть в консоли исполняемые
SQL-запросы и вообще всю внутрянку, например:
```
In [1]: from app import app, db, QuoteModel
In [2]: app.app_context().push()
In [3]: QuoteModel.query.all()
2024-03-12 21:14:09,668 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2024-03-12 21:14:09,674 INFO sqlalchemy.engine.Engine SELECT quotes.id AS quotes_id, quotes.author AS quotes_author, quotes.text AS quotes_text 
FROM quotes
2024-03-12 21:14:09,674 INFO sqlalchemy.engine.Engine [generated in 0.00054s] ()
Out[3]: []
```

## Стандартные запросы SQLAlchemy

1. Получить все цитаты
- QuoteModel.query.all()
- db.session.query(QuoteModel).all()
2. Получить цитату по id
- QuoteModel.query.get(id)
3. Получить все заметки с автором “Tom”
- QuoteModel.query.filter_by(author = “Tom”)
- QuoteModel.query.filter(QuoteModel.author==“Tom”)

## Связанные запросы SQLAlchemy
1. Найти все цитаты с именем автора Tom
- QuoteModel.query.filter(QuoteModel.author.has(name='Tom')).all()
- QuoteModel.query.join(QuoteModel.author).filter(QuoteModel.name == 'Tom').all()

## Составные запросы SQLAlchemy
1. Найти всех авторов с именами ‘Вася’ или ‘Петя’
- 1.1
AuthorModel.query.filter(
 (AuthorModel.name=='Вася') | (AuthorModel.name=='Петя')
)
- 1.2
from sqlalchemy import or_
AuthorModel.query.filter(
 or_(AuthorModel.name=='Вася', AuthorModel.name=='Петя')
) 


## Добавили параметр nullable=False в QuoteModel
author = db.Column(db.String(32), unique=False, nullable=False)
text = db.Column(db.String(255), unique=False, nullable=False)
// Теперь необходимо пересоздать БД, т.к. мы изменили существующие поля модели

## Удаляем БД и единственную существующую миграцию
main.db
74602cd88f5f_initial_migrations.py

## Заново создаем миграцию и накатываем БД
- flask db migrate -m "00001_initial migrations"
// ЗА СЧЕТ app.config['SQLALCHEMY_ECHO'] = True ВИДИМ ВСЮ ВНУТРЯНКУ:
```
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [sqlalchemy.engine.Engine] BEGIN (implicit)
INFO  [sqlalchemy.engine.Engine] PRAGMA main.table_info("alembic_version")
INFO  [sqlalchemy.engine.Engine] [raw sql] ()
INFO  [sqlalchemy.engine.Engine] PRAGMA temp.table_info("alembic_version")
INFO  [sqlalchemy.engine.Engine] [raw sql] ()
INFO  [sqlalchemy.engine.Engine] PRAGMA main.table_info("alembic_version")
INFO  [sqlalchemy.engine.Engine] [raw sql] ()
INFO  [sqlalchemy.engine.Engine] PRAGMA temp.table_info("alembic_version")
INFO  [sqlalchemy.engine.Engine] [raw sql] ()
INFO  [sqlalchemy.engine.Engine] 
CREATE TABLE alembic_version (
	version_num VARCHAR(32) NOT NULL, 
	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
)

INFO  [sqlalchemy.engine.Engine] [no key 0.00050s] ()
INFO  [sqlalchemy.engine.Engine] SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite~_%' ESCAPE '~' ORDER BY name
INFO  [sqlalchemy.engine.Engine] [raw sql] ()
INFO  [alembic.autogenerate.compare] Detected added table 'quotes'
INFO  [sqlalchemy.engine.Engine] ROLLBACK
  Generating /home/user/Projects/Flask1/Less5/migrations/versions/590454baad92_0001_initial_
  migrations.py ...  done
```

- flask db upgrade
```
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [sqlalchemy.engine.Engine] BEGIN (implicit)
INFO  [sqlalchemy.engine.Engine] PRAGMA main.table_info("alembic_version")
INFO  [sqlalchemy.engine.Engine] [raw sql] ()
INFO  [sqlalchemy.engine.Engine] SELECT alembic_version.version_num 
FROM alembic_version
INFO  [sqlalchemy.engine.Engine] [generated in 0.00037s] ()
INFO  [sqlalchemy.engine.Engine] PRAGMA main.table_info("alembic_version")
INFO  [sqlalchemy.engine.Engine] [raw sql] ()
INFO  [alembic.runtime.migration] Running upgrade  -> 590454baad92, 0001_initial_migrations
INFO  [sqlalchemy.engine.Engine] 
CREATE TABLE quotes (
	id INTEGER NOT NULL, 
	author VARCHAR(32) NOT NULL, 
	text VARCHAR(255) NOT NULL, 
	PRIMARY KEY (id)
)

INFO  [sqlalchemy.engine.Engine] [no key 0.00017s] ()
INFO  [sqlalchemy.engine.Engine] INSERT INTO alembic_version (version_num) VALUES ('590454baad92') RETURNING version_num
INFO  [sqlalchemy.engine.Engine] [generated in 0.00128s] ()
INFO  [sqlalchemy.engine.Engine] COMMIT
```

## Открываем БД в Antares и добавляем данные используя SQL-запросы quotes.sql

## Запускаем python app.py и проверяем что все работает

## NB
Пиши код исходя из того, что тебе приходят верные данные
Валидацию выделяй в отдельный блок