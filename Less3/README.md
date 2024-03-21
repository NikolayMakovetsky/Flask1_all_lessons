## Установка CLI клиент для sqlite3
```
sudo apt install sqlite3
```
## Создание БД и загрузка данных в терминале
```
sqlite3 quotes.db ".read init_database/quotes_db.sql"
```

## Работа с командной строкой в Linux
...$ mkdir Students (создание каталога)
...$ cd $_ (переход во вновь созданный каталог)

## Работа с Git

##  Примеры SQL-запросов
SELECT * FROM quotes;
SELECT * FROM quotes WHERE id IN (1,2,5)   //вместо 1,2,5 можно селект написать

// МАСКИ в SQL-запросах: (простые примеры) LIKE, NOT LIKE
SELECT * FROM quotes WHERE author LIKE '%Tom%'
SELECT * FROM quotes WHERE author LIKE '%tom%'
SELECT * FROM quotes WHERE author LIKE 'Tom22_' должен быть один символ после Tom22

--SELECT * FROM quotes WHERE id = 2;
UPDATE quotes SET author = 'Tom2' WHERE id = 24;
UPDATE quotes SET author = 'Tom2', text = 'Toms quote 2', rating = 4 WHERE id = 24;

// Удобное правило форматирования с использованием ТАБ
UPDATE  quotes
SET     author = 'Tom2',
        text = 'Toms quote 2',
        rating = 4
WHERE   1=1
--AND     id = 24
AND     id = 25
;

SELECT  author,
        rating,
        rating * 10 AS new_rating
FROM    quotes
WHERE   rating < 2;

INSERT INTO quotes (rating, author, text)
SELECT 2, 'Author4', 'text4' UNION ALL
SELECT 3, 'Author5', 'text5';

/*
INSERT INTO quotes (rating, author, text) VALUES
(2, 'Author4', 'text4'), 
(3, 'Author5', 'text5');
*/

INSERT INTO quotes (id, rating, author, text) VALUES
(null, 2, 'AuthorAUTO', 'textAUTO');
(11, 3, 'Author2', 'text2');

DELETE FROM quotes WHERE NOT id BETWEEN 1 and 4;

// BETWEEN включает граничные значения []
// имена полей необходимо писать в нижнем регистре
// Постгрес регистрозависимая БД
// Составные поля записываются с нижн подчеркиванием: language_code
// -- комментарий строки /* */ многострочный комментарий или коммент внутри строки
