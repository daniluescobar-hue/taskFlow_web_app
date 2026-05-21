import sqlite3

conn = sqlite3.connect("taskflow.db")

cursor = conn.cursor()

# TABLA USUARIOS

cursor.execute("""

CREATE TABLE IF NOT EXISTS users (

    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL

)

""")

# TABLA TAREAS

cursor.execute("""

CREATE TABLE IF NOT EXISTS tasks (

    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    title TEXT NOT NULL,
    priority TEXT,
    due_date TEXT,
    completed INTEGER DEFAULT 0

)

""")

conn.commit()

conn.close()

print("Base de datos creada correctamente.")