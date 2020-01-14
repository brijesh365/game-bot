import sqlite3

import settings


def run_query(query, parameters=()):
    with sqlite3.connect(settings.DEFAULT_PATH) as conn:
        cursor = conn.cursor()
        query_result = cursor.execute(query, parameters)
        conn.commit()
    return query_result


def fetch_user_id(name):
    queryset = run_query(f'SELECT id from user where name="{name}"')
    output = queryset.fetchone()
    return output[0] if output else None


def create_user(name):
    queryset = run_query(f'INSERT INTO user (name) VALUES ("{name}")')
    return queryset.fetchone()


def save_keyword(username, keyword):
    user_id = fetch_user_id(username)
    if not user_id:
        user_id = create_user(username)
    run_query(f'INSERT INTO history (user_id, keyword) VALUES ("{user_id}", "{keyword}")')


def fetch_history(username, keyword):
    user_id = fetch_user_id(username)
    if not user_id:
        user_id = create_user(username)
    queryset = run_query(f'SELECT keyword from history where user_id="{user_id}" and keyword LIKE "%{keyword}%"')
    output = queryset.fetchall()
    return ', '.join((ele[0] for ele in output))
