import psycopg2

import settings


def singleton(func):
    db_connection = None

    def get_connection(*args, **kwargs):
        if not db_connection:
            db_connection = func(*args, **kwargs)
        return db_connection

    return get_connection


@singleton
def get_db_connection():
    """Gets the db connection.

    :return: Database connection
    """
    try:
        connection = psycopg2.connect(user=settings.DB_USERNAME,
                                      password=settings.DB_PASSWORD,
                                      host=settings.DB_HOST,
                                      port="5432",
                                      database=settings.DB_NAME)
        connection.autocommit = True
        return connection
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
