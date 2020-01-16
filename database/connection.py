import psycopg2

import settings

db_connection = None


def get_db_connection():
    """Gets the db connection.

    :return: Database connection
    """
    global db_connection
    if db_connection:
        return db_connection
    try:
        db_connection = psycopg2.connect(user=settings.DB_USERNAME,
                                         password=settings.DB_PASSWORD,
                                         host=settings.DB_HOST,
                                         port="5432",
                                         database=settings.DB_NAME)
        db_connection.autocommit = True
        return db_connection
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
