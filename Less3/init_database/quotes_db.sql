/* Команда для создания БД
sqlite3 quotes.db ".read init_database/quotes_db.sql" */

PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;
CREATE TABLE quotes (
id INTEGER PRIMARY KEY AUTOINCREMENT,
rating INTEGER NOT NULL,
author TEXT NOT NULL,
text TEXT NOT NULL
);
INSERT INTO quotes VALUES(1,1,'Rick Cook','Программирование сегодня — это гонка разработчиков программ...');
INSERT INTO quotes VALUES(2,1,'Waldi Ravens','Программирование на С похоже на быстрые танцы на только...');
INSERT INTO quotes VALUES(3,1,'Mosher’s Law of Software Engineering','Не волнуйтесь, если что-то не работает. Если бы всё работало, вас бы уволили.');
INSERT INTO quotes VALUES(4,1,'Yoggi Berra','В теории, теория и практика неразделимы. На практике это не так.');
COMMIT;
