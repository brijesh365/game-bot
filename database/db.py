import psycopg2


def run_query(query):
    print(query)
    try:
        connection = psycopg2.connect(user="jkkfsrnjtmeyat",
                                      password="b2d8098aa62c8e3b99199a4dda5dbb83ae1cdf9d2d4cf7d960715d7451da4a6d",
                                      host="ec2-174-129-33-14.compute-1.amazonaws.com",
                                      port="5432",
                                      database="d9f2m20h3n4q4h")
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
