from database import db


def create_tables():
    db.run_query('''CREATE TABLE IF NOT EXISTS user
             (ID INTEGER  PRIMARY KEY  AUTOINCREMENT,
             NAME  TEXT  NOT NULL
             )
    ''')


def search_history():
    db.run_query('''CREATE TABLE IF NOT EXISTS history
                 (ID INTEGER  PRIMARY KEY  AUTOINCREMENT,
                 user_id INT,
                 keyword  TEXT  NOT NULL,
                 FOREIGN KEY (user_id)
                REFERENCES parent(id)
                ON DELETE CASCADE
                 )
        ''')


if __name__ == '__main__':
    create_tables()
    search_history()
