import sqlite3

def get_connection():
    conn = sqlite3.connect("tracker.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fields (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            application_id INTEGER NOT NULL,
            field_name TEXT NOT NULL,
            field_type TEXT NOT NULL,
            FOREIGN KEY (application_id) REFERENCES applications(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            field_id INTEGER NOT NULL,
            value TEXT,
            FOREIGN KEY (field_id) REFERENCES fields(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS home_columns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            field_name TEXT NOT NULL UNIQUE
        )
    """)

    conn.commit()
    conn.close()

def get_application(app_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM applications WHERE id = ?", (app_id,))
    app = cursor.fetchone()
    conn.close()
    return app

def add_application(name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO applications (name) VALUES (?)", (name,))
    app_id = cursor.lastrowid

    default_fields = [
        ("Status",           "choice", "Did not apply yet"),
        ("Company",          "text",   ""),
        ("Date Applied",     "date",   ""),
        ("Position",         "text",   ""),
        ("Deadline",         "date",   ""),
        ("Application Link", "text",   ""),
        ("Location",         "text",   ""),
        ("Duration",         "text",   ""),
        ("Salary",           "number", ""),
    ]

    for field_name, field_type, default_value in default_fields:
        cursor.execute("""
            INSERT INTO fields (application_id, field_name, field_type)
            VALUES (?, ?, ?)
        """, (app_id, field_name, field_type))

        cursor.execute("""
            INSERT INTO entries (field_id, value)
            VALUES (?, ?)
        """, (cursor.lastrowid, default_value))
        default_columns = ["Status", "Company", "Position", "Deadline"]
        for col in default_columns:
            cursor.execute("""
                INSERT OR IGNORE INTO home_columns (field_name) VALUES (?)
            """, (col,))
    conn.commit()
    conn.close()
    return app_id

def get_all_applications():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM applications")
    apps = cursor.fetchall()
    conn.close()
    return apps

def get_fields_and_values(app_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT fields.id, fields.field_name, fields.field_type, entries.value, entries.id as entry_id
        FROM fields
        LEFT JOIN entries ON entries.field_id = fields.id
        WHERE fields.application_id = ?
    """, (app_id,))

    results = cursor.fetchall()
    conn.close()
    return results

def add_field(app_id, field_name, field_type):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO fields (application_id, field_name, field_type)
        VALUES (?, ?, ?)
    """, (app_id, field_name, field_type))

    field_id = cursor.lastrowid

    cursor.execute("""
        INSERT INTO entries (field_id, value)
        VALUES (?, ?)
    """, (field_id, ""))

    conn.commit()
    conn.close()

def delete_field(field_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM entries WHERE field_id = ?", (field_id,))
    cursor.execute("DELETE FROM fields WHERE id = ?", (field_id,))
    conn.commit()
    conn.close()

def update_value(entry_id, new_value):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE entries SET value = ? WHERE id = ?", (new_value, entry_id))
    conn.commit()
    conn.close()

def delete_application(app_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM fields WHERE application_id = ?", (app_id,))
    fields = cursor.fetchall()

    for field in fields:
        cursor.execute("DELETE FROM entries WHERE field_id = ?", (field["id"],))

    cursor.execute("DELETE FROM fields WHERE application_id = ?", (app_id,))
    cursor.execute("DELETE FROM applications WHERE id = ?", (app_id,))

    conn.commit()
    conn.close()

def get_home_columns():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT field_name FROM home_columns")
    cols = [row["field_name"] for row in cursor.fetchall()]
    conn.close()
    return cols

def add_home_column(field_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO home_columns (field_name) VALUES (?)", (field_name,))
    conn.commit()
    conn.close()

def remove_home_column(field_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM home_columns WHERE field_name = ?", (field_name,))
    conn.commit()
    conn.close()
    
def rename_application(app_id, new_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE applications SET name = ? WHERE id = ?", (new_name, app_id))
    conn.commit()
    conn.close()