import psycopg2
import csv
from db.create_connection import create_connection as create_connection

def import_menu_from_csv():
    conn = create_connection()
    cursor = conn.cursor()
    
    with open("menu.csv", mode="r", encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            cursor.execute("""
                INSERT INTO menu (name, type, price)
                VALUES (%s, %s, %s)
            """, (row["name"], row["type"], row["price"]))
    
    conn.commit()
    conn.close()
    cursor.close()

def menu_cleaning():
    try:
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM menu;")
        conn.commit()

        deleted_rows = cursor.rowcount
        
        return deleted_rows > 0

    except psycopg2.Error as e:
        conn.rollback()
        raise e

    finally:
        if conn is not None:
            conn.close()
            cursor.close()