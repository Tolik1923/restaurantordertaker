import psycopg2
from db.create_connection import create_connection as create_connection

def get_menu_positions():
    try:
        conn = create_connection()
        with conn:
            with conn.cursor() as cursor:
                query = "SELECT name FROM menu"
                cursor.execute(query)
                positions = [row[0] for row in cursor.fetchall()]  
                return positions
    except (Exception, psycopg2.Error) as error:
        return None

def creating_order():
    try:
        conn = create_connection()
        with conn:
            with conn.cursor() as cursor:
                query = "INSERT INTO orders DEFAULT VALUES RETURNING id"
                cursor.execute(query)
                conn.commit() 
                order_id = cursor.fetchone()[0]
                return order_id
    except (Exception, psycopg2.Error) as error:
        return error


def creating_items(id_orders, item):
    try:
        conn = create_connection()
        with conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT price FROM menu WHERE name = %s;", (item,))
                price = cursor.fetchone()
                if price:
                    cursor.execute(
                        "INSERT INTO items (id_orders, name, price) VALUES (%s, %s, %s);",
                        (id_orders, item, price[0])
                    )
                    conn.commit()
                else:
                    return "Item not found in the menu."
    except (Exception, psycopg2.Error) as error:
        return error

def delete_items(id_orders, item):
    try:
        conn = create_connection()
        with conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM items WHERE ctid IN (SELECT ctid FROM items WHERE id_orders = %s AND name = %s LIMIT 1);", (id_orders, item))
                conn.commit()
                mes = "{} has been removed from the order. Would you like anything else?".format(item)
                return mes
    except (Exception, psycopg2.Error) as error:
        return {"message": error}
    
def get_total(id_orders):
    try:
        conn = create_connection()
        with conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT total FROM orders WHERE id = %s", (id_orders,))
                total = cursor.fetchone()
                if total:
                    mes = "Your total is ${}. Thank you and have a nice day!".format(total[0])
                    return mes
                else:
                    return "Order not found."
    except (Exception, psycopg2.Error) as error:
        return {"message": str(error)}

def get_dish_type(item):
    try:
        conn = create_connection()
        with conn:
            with conn.cursor() as cursor:
                query = "SELECT type FROM menu WHERE name = %s"
                cursor.execute(query, (item,))
                dish_type = cursor.fetchone()
                if dish_type:
                    dish_type = dish_type[0].lower()
                    if dish_type == 'dish':
                        return True
                    else:
                        return False
    except (Exception, psycopg2.Error) as error:
        return None
    
def chek_upsell_mes(id_orders):
    try:
        conn = create_connection()
        with conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id_orders FROM upsell WHERE id_orders = %s;", (id_orders,))
                existing_order = cursor.fetchone()

                if not existing_order:
                    cursor.execute(
                        "INSERT INTO upsell (id_orders) VALUES (%s);",
                        (id_orders,)
                    )
                    return True
                else:
                    return False
    except (Exception, psycopg2.Error) as error:
        print("Error:", error)


def send_upsell_mes(id_orders):
    try:
        conn = create_connection()
        with conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM menu WHERE type = 'drink';")
                count = cursor.fetchone()[0]
                if count > 0:
                    query = "SELECT name, price FROM menu WHERE type = 'drink' LIMIT 1;"
                    cursor.execute(query)
                    upsell = cursor.fetchone()
                    mes = "Would you like to add a {} for ${}?".format(upsell[0], upsell[1])
                    return mes, upsell[0]
                else:
                    return None, None
    except (Exception, psycopg2.Error) as error:
        print("Error:", error)

def input_history(guest_message, chat_message, id_orders):
    print(guest_message, chat_message, id_orders)
    try:
        conn = create_connection()
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO history (id_orders, who, replica) VALUES (%s, %s, %s);",
                    (id_orders, "guest", guest_message)
                )
                cursor.execute(
                    "INSERT INTO history (id_orders, who, replica) VALUES (%s, %s, %s);",
                    (id_orders, "chat", chat_message)
                )
                conn.commit()
    except (Exception, psycopg2.Error) as error:
        return error
