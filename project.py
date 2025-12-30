from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

def get_db():
    return sqlite3.connect("database.db")

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = cur.fetchone()

        if user:
            session["user_id"] = user[0]
            return redirect("/dashboard")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        cur = db.cursor()
        cur.execute("INSERT INTO users(email,password) VALUES(?,?)", (email, password))
        db.commit()
        return redirect("/")
    return render_template("register.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user_id" not in session:
        return redirect("/")

    db = get_db()
    cur = db.cursor()

    if request.method == "POST":
        task = request.form["task"]
        cur.execute("INSERT INTO tasks(user_id,task) VALUES(?,?)", (session["user_id"], task))
        db.commit()

    cur.execute("SELECT * FROM tasks WHERE user_id=?", (session["user_id"],))
    tasks = cur.fetchall()

    return render_template("dashboard.html", tasks=tasks)

@app.route("/done/<int:id>")
def done(id):
    db = get_db()
    cur = db.cursor()
    cur.execute("UPDATE tasks SET done=1 WHERE id=?", (id,))
    db.commit()
    return redirect("/dashboard")

@app.route("/delete/<int:id>")
def delete(id):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM tasks WHERE id=?", (id,))
    db.commit()
    return redirect("/dashboard")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
