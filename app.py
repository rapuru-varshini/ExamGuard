from flask import Flask, redirect, request, render_template, session
from database import init_db, get_db

app = Flask(__name__)
app.secret_key = "examguard_secret_key"

print(app.url_map)

init_db()


@app.route("/")
def home():
    return "Welcome to Exam Guard"


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        connection = get_db()

        connection.execute(
            """
            INSERT INTO candidates
            (name, email, password)
            VALUES (?, ?, ?)
            """,
            (name, email, password)
        )

        connection.commit()
        connection.close()

        return "Registration successful"

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        connection = get_db()

        candidate = connection.execute(
            """
            SELECT *
            FROM candidates
            WHERE email = ? AND password = ?
            """,
            (email, password)
        ).fetchone()

        connection.close()

        if candidate:
            session["candidate_id"] = candidate[0]
            return redirect("/dashboard")

        return "Invalid email or password"

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():

    if "candidate_id" not in session:
        return "Please login first"

    return render_template("dashboard.html")


@app.route("/logout")
def logout():

    session.clear()
    return redirect("/login")




if __name__ == "__main__":
    print(app.url_map)
    app.run(debug=True)