from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# --- Create database on start ---
conn = sqlite3.connect("database.db")
conn.execute("CREATE TABLE IF NOT EXISTS students(id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
conn.close()

@app.route("/")
def index():
    conn = sqlite3.connect("database.db")
    students = conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    return render_template("index.html", students=students)

@app.route("/add", methods=["POST"])
def add_student():
    name = request.form["name"]
    age = request.form["age"]
    conn = sqlite3.connect("database.db")
    conn.execute("INSERT INTO students(name, age) VALUES(?, ?)", (name, age))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/update/<int:id>", methods=["POST"])
def update_student(id):
    name = request.form["name"]
    age = request.form["age"]
    conn = sqlite3.connect("database.db")
    conn.execute("UPDATE students SET name=?, age=? WHERE id=?", (name, age, id))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/delete/<int:id>")
def delete_student(id):
    conn = sqlite3.connect("database.db")
    conn.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
