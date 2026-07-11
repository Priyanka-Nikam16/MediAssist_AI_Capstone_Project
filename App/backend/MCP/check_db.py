from connector import get_db_connection

def show_database():
    conn = get_db_connection()
    cursor = conn.cursor()

    
    # Get all tables
    cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)

    tables = cursor.fetchall()

    print("\n===== TABLES IN DATABASE =====")
    for table in tables:
        table_name = table[0]
        print(f"\n\n===== {table_name} =====")

        try:
            # Get column names
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 5")
            rows = cursor.fetchall()

            columns = [desc[0] for desc in cursor.description]
            print("Columns:")
            print(columns)

            print("\nSample Data:")
            for row in rows:
                print(row)

        except Exception as e:
            print(f"Error reading {table_name}: {e}")

    cursor.close()
    conn.close()


if __name__== "__main__":
    show_database()
