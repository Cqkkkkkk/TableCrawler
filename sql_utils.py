import sqlite3

def create_database_and_table(connection):
    cursor = connection.cursor()
    # Create table if it does not exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS table_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            table_name TEXT,
            url TEXT UNIQUE NOT NULL,
            location TEXT DEFAULT NULL
        )
    """)
    connection.commit()

def insert_table_info(connection, table_name, url):
    cursor = connection.cursor()
    # Insert table information
    cursor.execute("""
        INSERT OR IGNORE INTO table_info (table_name, url)
        VALUES (?, ?)
    """, (table_name, url))
    connection.commit()

def check_url_exists(connection, url):
    cursor = connection.cursor()
    # Check if the URL exists in the table
    cursor.execute("SELECT location FROM table_info WHERE url = ?", (url,))
    result = cursor.fetchone()
    if result:
        return True, result[0]
    return False, None

def update_location(connection, url, new_location):
    cursor = connection.cursor()
    # Update the location of a specific URL
    cursor.execute("UPDATE table_info SET location = ? WHERE url = ?", (new_location, url))
    connection.commit()

def update_table_name(connection, url, new_table_name):
    cursor = connection.cursor()
    # Update the table name of a specific URL
    cursor.execute("UPDATE table_info SET table_name = ? WHERE url = ?", (new_table_name, url))
    connection.commit()
    # print(f"Updated table name for {url} to {new_table_name}")

def fetch_undownloaded_url(connection):
    cursor = connection.cursor()
    # Fetch a URL with location as empty and table name as "undownloaded"
    cursor.execute("""
        SELECT url 
        FROM table_info 
        WHERE location IS NULL AND table_name = 'undownloaded'
        LIMIT 1
    """)
    result = cursor.fetchone()
    if result:
        return result[0]
    return None
