from flask import Flask, render_template, request, redirect, session
import sqlite3
import random

from datetime import datetime

app = Flask(__name__)

app.secret_key = "taskflow_secret_key"


# --------------------------------
# DATABASE
# --------------------------------

def connect_db():

    conn = sqlite3.connect("tasks.db")

    return conn


# --------------------------------
# CREATE TABLES
# --------------------------------

conn = connect_db()

cursor = conn.cursor()

cursor.execute("""

CREATE TABLE IF NOT EXISTS users (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT UNIQUE,

    password TEXT

)

""")

cursor.execute("""

CREATE TABLE IF NOT EXISTS tasks (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER,

    title TEXT,

    priority TEXT,

    due_date TEXT,

    completed INTEGER DEFAULT 0

)

""")

conn.commit()

conn.close()


# --------------------------------
# TASKBOT MESSAGES
# --------------------------------

messages = [

    "🤖 Estoy analizando tus próximas tareas.",

    "📚 Organizar tu tiempo mejora tu rendimiento.",

    "🔥 Cada tarea completada es un avance importante.",

    "🚀 Tu productividad está creciendo.",

    "⏰ Detecté actividades próximas esta semana.",

    "💡 Consejo: empieza por las tareas pequeñas.",

    "📌 Mantener un horario organizado reduce el estrés.",

    "🎯 Intenta completar al menos 3 tareas hoy.",

    "🧠 La constancia diaria genera mejores resultados.",

    "✨ TaskFlow AI está monitoreando tus entregas."

]


# --------------------------------
# LOGIN
# --------------------------------

@app.route("/", methods=["GET", "POST"])

def login():

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        conn = connect_db()

        cursor = conn.cursor()

        cursor.execute(

            "SELECT * FROM users WHERE username=? AND password=?",

            (username, password)

        )

        user = cursor.fetchone()

        conn.close()

        if user:

            session["user_id"] = user[0]

            session["username"] = user[1]

            return redirect("/dashboard")

        else:

            return render_template(

                "login.html",

                error="Usuario o contraseña incorrectos"

            )

    return render_template("login.html")


# --------------------------------
# REGISTER
# --------------------------------

@app.route("/register", methods=["GET", "POST"])

def register():

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        try:

            conn = connect_db()

            cursor = conn.cursor()

            cursor.execute(

                "INSERT INTO users (username, password) VALUES (?, ?)",

                (username, password)

            )

            conn.commit()

            conn.close()

            return render_template(

                "register.html",

                success="¡Usuario registrado correctamente!"

            )

        except:

            return render_template(

                "register.html",

                error="Ese usuario ya existe"

            )

    return render_template("register.html")


# --------------------------------
# DASHBOARD
# --------------------------------

@app.route("/dashboard")

def dashboard():

    if "user_id" not in session:

        return redirect("/")

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute(

        "SELECT * FROM tasks WHERE user_id=? ORDER BY due_date ASC",

        (session["user_id"],)

    )

    tasks = cursor.fetchall()

    conn.close()

    bot_message = random.choice(messages)

    return render_template(

        "index.html",

        tasks=tasks,

        username=session["username"],

        bot_message=bot_message

    )


# --------------------------------
# ADD TASK
# --------------------------------

@app.route("/add", methods=["POST"])

def add_task():

    if "user_id" not in session:

        return redirect("/")

    title = request.form["title"]

    due_date = request.form["due_date"]

    today = datetime.today()

    due = datetime.strptime(due_date, "%Y-%m-%d")

    days_left = (due - today).days

    if days_left <= 3:

        priority = "Alta"

    elif days_left <= 7:

        priority = "Media"

    else:

        priority = "Baja"

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute(

        """

        INSERT INTO tasks

        (user_id, title, priority, due_date)

        VALUES (?, ?, ?, ?)

        """,

        (

            session["user_id"],

            title,

            priority,

            due_date

        )

    )

    conn.commit()

    conn.close()

    return redirect("/dashboard")


# --------------------------------
# COMPLETE TASK
# --------------------------------

@app.route("/complete/<int:task_id>")

def complete_task(task_id):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute(

        "UPDATE tasks SET completed=1 WHERE id=?",

        (task_id,)

    )

    conn.commit()

    conn.close()

    return redirect("/dashboard")


# --------------------------------
# DELETE TASK
# --------------------------------

@app.route("/delete/<int:task_id>")

def delete_task(task_id):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute(

        "DELETE FROM tasks WHERE id=?",

        (task_id,)

    )

    conn.commit()

    conn.close()

    return redirect("/dashboard")


# --------------------------------
# LOGOUT
# --------------------------------

@app.route("/logout")

def logout():

    session.clear()

    return redirect("/")


# --------------------------------
# RUN APP
# --------------------------------

if __name__ == "__main__":

    app.run(debug=True)