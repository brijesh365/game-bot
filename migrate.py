"""
Creates initial tables required by the app.
"""
from database import db


def create_users_tables():
    """Creates Users table

    :return: None
    """
    db.run_query('''
    CREATE TABLE IF NOT EXISTS users (
        ID SERIAL PRIMARY KEY NOT NULL,
        NAME  TEXT  NOT NULL
    );
''')


def create_search_history():
    """Create history table.

    :return: None
    """
    db.run_query('''CREATE TABLE IF NOT EXISTS history
                 (ID SERIAL PRIMARY KEY,
                 user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                 keyword  TEXT  NOT NULL,
                 updated_on TIMESTAMP NOT NULL default CURRENT_TIMESTAMP,
                 CONSTRAINT user_keyword_constraint UNIQUE(user_id, keyword)
                 );
        ''')


if __name__ == '__main__':
    create_users_tables()
    create_search_history()
