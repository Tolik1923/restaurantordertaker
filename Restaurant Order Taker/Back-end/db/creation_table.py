import psycopg2
from db.create_connection import create_connection as create_connection

def create_database_objects():
    connection = create_connection()
    if connection is None:
        return

    try:
        cursor = connection.cursor()

        create_menu_table_query = """
            CREATE TABLE IF NOT EXISTS menu (
                name VARCHAR(255) NOT NULL,
                type VARCHAR(255) NOT NULL,
                price DECIMAL(10, 2) NOT NULL
            );
        """
        cursor.execute(create_menu_table_query)

        create_orders_table_query = """
            CREATE TABLE IF NOT EXISTS orders (
                id SERIAL PRIMARY KEY,
                total DECIMAL(10, 2) DEFAULT 0.00
            );
        """
        cursor.execute(create_orders_table_query)

        create_orders_upsell_query = """
            CREATE TABLE IF NOT EXISTS upsell (
                id_orders INT REFERENCES orders(id)
            );
        """
        cursor.execute(create_orders_upsell_query)

        create_items_table_query = """
            CREATE TABLE IF NOT EXISTS items (
                id_orders INT REFERENCES orders(id),
                name VARCHAR(255) NOT NULL,
                price DECIMAL(10, 2),
                FOREIGN KEY (id_orders) REFERENCES orders(id)
            );

            CREATE OR REPLACE FUNCTION update_order_total() RETURNS TRIGGER AS $$
            BEGIN
                IF TG_OP = 'INSERT' THEN
                    UPDATE orders
                    SET total = total + NEW.price
                    WHERE id = NEW.id_orders;
                ELSIF TG_OP = 'DELETE' THEN
                    UPDATE orders
                    SET total = total - OLD.price
                    WHERE id = OLD.id_orders;
                END IF;
                
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;

            DO $$
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'update_order_total_trigger') THEN
                    CREATE TRIGGER update_order_total_trigger
                    AFTER INSERT OR DELETE ON items
                    FOR EACH ROW
                    EXECUTE FUNCTION update_order_total();
                END IF;
            END;
            $$;

        """
        cursor.execute(create_items_table_query)
        
        create_history_table_query = """
            CREATE TABLE IF NOT EXISTS history (
                id_orders INT REFERENCES orders(id),
                who VARCHAR(255) NOT NULL,
                replica VARCHAR(255) NOT NULL
            );
        """
        cursor.execute(create_history_table_query)

        connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Error", error)

    finally:
        if connection:
            cursor.close()
            connection.close()
