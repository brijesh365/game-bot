from database import connection


def run_query(query):
    """Runs the given query on database.

    :param query: Query needs to be run database
    :return: Database cursor
    """
    conn = connection.get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor


def fetch_user_id(name):
    """Fetches the user ID.

    :param name: The name of user for whom ID needs to fetch.
    :return: The user ID or None.
    """
    queryset = run_query(f"SELECT id from users where name='{name}'")
    output = queryset.fetchone()
    return output[0] if output else None


def create_user(name):
    """Creates user in database.

    :param name: Name of the user.
    :return: The ID of newly created user.
    """
    queryset = run_query(f'INSERT INTO users (name) VALUES (\'{name}\') RETURNING id')
    return queryset.fetchone()[0]


def save_keyword(username, keyword):
    """Saves the search keyword for a given user.

    :param username: Name of the user.
    :param keyword: The search keyword.
    :return: None
    """
    user_id = fetch_user_id(username)
    if not user_id:
        user_id = create_user(username)
    run_query(
        f'INSERT INTO history (user_id, keyword, updated_on) VALUES (\'{user_id}\', \'{keyword}\', NOW()) ON CONFLICT ON CONSTRAINT user_keyword_constraint DO UPDATE SET updated_on = NOW()'
    )


def fetch_history(username, keyword):
    """Fetches most recent search history for a given user and for given keyword.

    :param username: Name of the user.
    :param keyword: The search keyword.
    :return: Top 5 search results.
    """
    user_id = fetch_user_id(username)
    if not user_id:
        user_id = create_user(username)
    queryset = run_query(
        f"SELECT keyword from history where user_id='{user_id}' and keyword LIKE '%{keyword}%' ORDER BY updated_on DESC"
    )
    output = queryset.fetchall()
    return ', '.join((ele[0] for ele in output))
