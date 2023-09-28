import psycopg2
from db.config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

def create_connection():
    try:
        connection = psycopg2.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME
        )
        return connection
    except (Exception, psycopg2.Error) as error:
        print("Error", error)
        return None
