import psycopg2
import db.for_guest as for_guest
from db.create_connection import create_connection as create_connection

def get_all_submitted_orders():
    answer = {}
    try:
        conn = create_connection()
        with conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id FROM orders")
                result_tuples = cursor.fetchall()
                id_orders = [int(item[0]) for item in result_tuples]
                
                for id in id_orders:
                    cursor.execute("SELECT total FROM orders WHERE id=%s", (id,))
                    s = f"Total - {id}"
                    answer.update({s: float(cursor.fetchone()[0])})

                    cursor.execute("SELECT name FROM items WHERE id_orders=%s", (id,))
                    result_tuples = cursor.fetchall()
                    result = [item[0] for item in result_tuples]
                    s = f"all items - {id}"
                    answer.update({s: result})

                    s = f"The history - {id}"
                    answer.update({s: ""})
                    cursor.execute("SELECT * FROM history WHERE id_orders=%s", (id,))
                    rows = cursor.fetchall()
                    x = 0
                
                    for row in rows:
                        x += 1
                        row_key = f"{row[0]} - {x}"
                        row_string = f"{row[1]} - {row[2]}"  
                        answer.update({row_key : row_string})

    except (Exception, psycopg2.Error) as error:
        return None
    
    finally:
        cursor.close()
        conn.close()

    return answer
    
def get_general_order_stats():
    stats = {}
    try:
        conn = create_connection()
        with conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM orders;")
                stats.update({"Total amount": cursor.fetchone()[0]})

                cursor.execute("SELECT SUM(total) FROM orders")
                stats.update({"Total revenue": float(cursor.fetchone()[0])})
                
                average = round((stats["Total revenue"]/stats["Total amount"]), 2)
                stats.update({"Average order price": average})

                positions = for_guest.get_menu_positions()
                #positions = ['lamb', 'steak', 'risotto', 'foie gras', 'red wine']
                for item in positions:
                    cursor.execute("SELECT COUNT(*) FROM items WHERE name = %s;", (item,))
                    stats.update({item: cursor.fetchone()[0]})

                stats.update({"Upsell stats": ""})
                cursor.execute("SELECT COUNT(*) FROM history WHERE replica = 'Would you like to add a red wine for $0.70?' ;")
                stats.update({"questions": cursor.fetchone()[0]})

                cursor.execute("SELECT COUNT(*) FROM history WHERE replica = 'yes, please' ;")
                stats.update({"accepted": cursor.fetchone()[0]})

                cursor.execute("SELECT COUNT(*) FROM history WHERE replica = 'no, thank you' ;")
                stats.update({"rejected": cursor.fetchone()[0]})

                upsell_revenue = stats["accepted"] * 0.70
                stats.update({"upsell_revenue": upsell_revenue})
    
    except (Exception, psycopg2.Error) as error:
        return None

    finally:
        cursor.close()
        conn.close()

    return stats
