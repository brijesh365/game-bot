import psycopg2

import settings


def run_query(query):
    print(query)
    try:
        connection = psycopg2.connect(user=settings.DB_USERNAME,
                                      password=settings.DB_PASSWORD,
                                      host=settings.DB_HOST,
                                      port="5432",
                                      database=settings.DB_NAME)
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    else:
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute(query)
        return cursor
    # finally:
    #     if (connection):
    #         cursor.close()
    #         connection.close()


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
    run_query(
        f'INSERT INTO history (user_id, keyword) VALUES ("{user_id}", "{keyword}" ON CONFLICT ON CONSTRAINT user_keyword_constraint DO UPDATE SET updated_on = NOW()'
    )


def fetch_history(username, keyword):
    user_id = fetch_user_id(username)
    if not user_id:
        user_id = create_user(username)
    queryset = run_query(
        f'SELECT keyword from history where user_id="{user_id}" and keyword LIKE "%{keyword}%" ORDER BY updated_on DESC'
    )
    output = queryset.fetchall()
    return ', '.join((ele[0] for ele in output))
