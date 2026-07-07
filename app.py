import os
from flask import Flask, render_template, request, redirect, session, flash, url_for
import bcrypt
import fitz
from werkzeug.utils import secure_filename

from database import users, summaries
from summarizer import generate_summary
from keypoints import extract_keypoints
from easy_summary import simplify_text
from table_detector import detect_tables
from graph_explainer import explain_graphs
from keywords import extract_keywords   # ⭐ NEW

app = Flask(__name__)
app.secret_key = "supersecretkey"

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf"}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("home.html")


# ---------------- SIGNUP ----------------
@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if users.find_one({"username": username}):
            flash("Username already exists")
            return redirect(url_for("signup"))

        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        users.insert_one({
            "username": username,
            "password": hashed
        })

        flash("Signup Successful. Please Login.")
        return redirect(url_for("login"))

    return render_template("signup.html")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        user = users.find_one({"username": username})

        if user and bcrypt.checkpw(password.encode("utf-8"), user["password"]):
            session["user"] = username
            return redirect(url_for("dashboard"))

        flash("Invalid Login")

    return render_template("login.html")


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect(url_for("login"))

    history = list(summaries.find({"username": session["user"]}).sort("_id", -1))

    return render_template("dashboard.html", history=history)


# ---------------- UPLOAD ----------------
@app.route("/upload", methods=["POST"])
def upload():

    if "user" not in session:
        return redirect(url_for("login"))

    if "pdf" not in request.files:
        flash("No file selected")
        return redirect(url_for("dashboard"))

    pdf = request.files["pdf"]

    if pdf.filename == "":
        flash("No file selected")
        return redirect(url_for("dashboard"))

    if not allowed_file(pdf.filename):
        flash("Only PDF allowed")
        return redirect(url_for("dashboard"))

    filename = secure_filename(pdf.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    pdf.save(filepath)

    try:
        doc = fitz.open(filepath)
    except:
        flash("Invalid PDF")
        return redirect(url_for("dashboard"))

    page_results = []
    full_text = ""

    for i, page in enumerate(doc):

        text = page.get_text()

        if not text or not text.strip():
            continue

        full_text += text

        summary = generate_summary(text)
        easy_summary = simplify_text(summary)
        keypoints = extract_keypoints(text)
        keywords = extract_keywords(text)   # ⭐ NEW
        graph_explanation = explain_graphs(text)

        page_results.append({
            "page": i + 1,
            "summary": summary,
            "easy": easy_summary,
            "keypoints": keypoints,
            "keywords": keywords,
            "graph": graph_explanation
        })

    tables = detect_tables(filepath)

    overall_summary = generate_summary(full_text) if full_text else "No text found"

    summaries.insert_one({
        "username": session["user"],
        "file": filename,
        "overall_summary": overall_summary
    })

    return render_template(
        "summary.html",
        pages=page_results,
        overall=overall_summary,
        tables=tables,
        filename=filename
    )



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)