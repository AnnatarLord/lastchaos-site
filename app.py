from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Поменяй на свой!

GUIDES_FILE = "guides.json"

def load_guides():
    if os.path.exists(GUIDES_FILE):
        with open(GUIDES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_guides(data):
    with open(GUIDES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app.route("/")
def index():
    return redirect(url_for("guides"))

@app.route("/guides", methods=["GET", "POST"])
def guides():
    guides = load_guides()
    selected_class = request.form.get("class_select")
    guide_text = ""
    if selected_class:
        guide_text = guides.get(selected_class, "Гайд отсутствует.")
    return render_template("guides.html", guides=guides, selected_class=selected_class, guide_text=guide_text)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "admin":
            session["logged_in"] = True
            return redirect(url_for("admin"))
        else:
            return render_template("login.html", error="Неверный логин или пароль")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("login"))

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    guides = load_guides()
    selected_class = request.form.get("class_select")
    guide_text = ""

    if request.method == "POST" and "save" in request.form:
        new_text = request.form.get("guide_text")
        if selected_class:
            guides[selected_class] = new_text
            save_guides(guides)
    if selected_class:
        guide_text = guides.get(selected_class, "")
    return render_template("admin.html", guides=guides, selected_class=selected_class, guide_text=guide_text)

if __name__ == "__main__":
    app.run(debug=True)