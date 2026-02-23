from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import numpy as np
from sklearn.linear_model import LinearRegression

app = Flask(__name__)
app.secret_key = "supersecretkey"

# -------------------------------
# ML Model
# -------------------------------
X = np.array([
    [80, 4, 70],
    [60, 2, 50],
    [90, 6, 85],
    [50, 1, 40],
    [75, 3, 65]
])
y = np.array([78, 55, 88, 45, 72])

model = LinearRegression()
model.fit(X, y)

# -------------------------------
# Routes
# -------------------------------

@app.route("/")
def login():
    return render_template("login.html")


@app.route("/home")
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def do_login():
    username = request.form["username"]
    password = request.form["password"]

    # Simple static login (you can upgrade later)
    if username == "admin" and password == "1234":
        session["user"] = username
        return redirect(url_for("home"))
    else:
        return "Invalid Credentials"


@app.route("/submit", methods=["POST"])
def submit():
    if "user" not in session:
        return redirect(url_for("login"))

    attendance = int(request.form["attendance"])
    study_hours = int(request.form["study_hours"])
    internal_marks = int(request.form["internal_marks"])

    prediction = model.predict([[attendance, study_hours, internal_marks]])
    score = round(prediction[0], 2)

    if score >= 75:
        result = "Grade A"
    elif score >= 60:
        result = "Grade B"
    elif score >= 40:
        result = "Grade C"
    else:
        result = "FAIL"

    # 🔥 STEP 1 DATABASE SAVE (ADD THIS PART)
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS records (
        attendance INT,
        study_hours INT,
        internal_marks INT,
        score REAL,
        result TEXT
    )
    """)

    cursor.execute("INSERT INTO records VALUES (?, ?, ?, ?, ?)",
                   (attendance, study_hours, internal_marks, score, result))

    conn.commit()
    conn.close()

    return render_template(
        "result.html",
        attendance=attendance,
        study_hours=study_hours,
        internal_marks=internal_marks,
        score=score,
        result=result
    )


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)