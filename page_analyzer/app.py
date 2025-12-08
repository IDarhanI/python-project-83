import os

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for

from . import db
from .checker import check_website
from .validators import normalize_url, validate_url

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/urls", methods=["GET"])
def urls():
    urls_list = db.get_all_urls()
    return render_template("urls.html", urls=urls_list)


@app.route("/urls/<int:id>")
def url_detail(id):
    url = db.get_url_by_id(id)
    if not url:
        flash("Страница не найдена", "danger")
        return redirect(url_for("urls"))

    checks = db.get_url_checks(id)
    return render_template("url.html", url=url, checks=checks)


@app.route("/urls", methods=["POST"])
def add_url():
    url = request.form.get("url", "").strip()

    error = validate_url(url)
    if error:
        flash(error, "danger")
        return render_template("index.html", url=url), 422

    normalized_url = normalize_url(url)
    existing_url = db.get_url_by_name(normalized_url)

    if existing_url:
        flash("Страница уже существует", "info")
        return redirect(url_for("url_detail", id=existing_url["id"]))

    try:
        url_id = db.add_url(normalized_url)
        flash("Страница успешно добавлена", "success")
        return redirect(url_for("url_detail", id=url_id))
    except Exception:
        flash("Произошла ошибка при добавлении URL", "danger")
        return render_template("index.html", url=url), 500


@app.route("/urls/<int:id>/checks", methods=["POST"])
def add_check(id):
    # Получаем URL из базы данных
    url_data = db.get_url_by_id(id)
    if not url_data:
        flash("Сайт не найден", "danger")
        return redirect(url_for("urls"))

    url = url_data["name"]

    # Проверяем сайт с помощью checker.py
    check_data = check_website(url)

    if not check_data:
        flash("Произошла ошибка при проверке", "danger")
        return redirect(url_for("url_detail", id=id))

    # Сохраняем проверку с данными
    try:
        check = db.add_url_check_with_data(id, check_data)
        if check:
            flash("Страница успешно проверена", "success")
        else:
            flash("Произошла ошибка при сохранении проверки", "danger")
    except Exception:
        flash("Произошла ошибка при сохранении проверки", "danger")

    return redirect(url_for("url_detail", id=id))
