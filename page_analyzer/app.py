import os
from datetime import datetime
from urllib.parse import urlparse

import psycopg2
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

DATABASE_URL = os.getenv("DATABASE_URL")


def is_valid_url(url):
    if len(url) > 255:
        return False
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def normalize_url(url):
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"


def get_connection():
    return psycopg2.connect(DATABASE_URL)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/urls", methods=["POST"])
def add_url():
    url = request.form.get("url", "").strip()

    if not url:
        flash("URL обязателен", "danger")
        return render_template("index.html", url=url), 422

    if not is_valid_url(url):
        flash("Некорректный URL", "danger")
        return render_template("index.html", url=url), 422

    normalized_url = normalize_url(url)

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM urls WHERE name = %s", (normalized_url,))
            existing = cur.fetchone()

            if existing:
                url_id = existing[0]
                flash("Страница уже существует", "info")
            else:
                created_at = datetime.now()
                cur.execute(
                    "INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING id",
                    (normalized_url, created_at),
                )
                url_id = cur.fetchone()[0]
                conn.commit()
                flash("Страница успешно добавлена", "success")

    return redirect(url_for("show_url", id=url_id))


@app.route("/urls")
def urls():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT 
                    urls.id, 
                    urls.name,
                    MAX(url_checks.created_at) as last_check_date,
                    (SELECT status_code 
                     FROM url_checks 
                     WHERE url_id = urls.id 
                     ORDER BY created_at DESC 
                     LIMIT 1) as last_check_status
                FROM urls
                LEFT JOIN url_checks ON urls.id = url_checks.url_id
                GROUP BY urls.id, urls.name
                ORDER BY urls.created_at DESC
            """
            )
            urls_list = cur.fetchall()

    return render_template("urls_index.html", urls=urls_list)


@app.route("/urls/<int:id>")
def show_url(id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            # Получаем информацию о сайте
            cur.execute("SELECT id, name, created_at FROM urls WHERE id = %s", (id,))
            url_data = cur.fetchone()

            if not url_data:
                flash("URL не найден", "danger")
                return redirect(url_for("urls"))

            # Получаем все проверки для этого сайта
            cur.execute(
                """
                SELECT id, status_code, h1, title, description, created_at
                FROM url_checks
                WHERE url_id = %s
                ORDER BY created_at DESC
            """,
                (id,),
            )
            checks = cur.fetchall()

    return render_template("urls_show.html", url=url_data, checks=checks)


@app.route("/urls/<int:id>/checks", methods=["POST"])
def check_url(id):
    # На этом шаге просто создаем запись о проверке без реальной проверки
    created_at = datetime.now()

    with get_connection() as conn:
        with conn.cursor() as cur:
            # Проверяем, существует ли URL
            cur.execute("SELECT id FROM urls WHERE id = %s", (id,))
            if not cur.fetchone():
                flash("URL не найден", "danger")
                return redirect(url_for("urls"))

            # Временно создаем проверку без реальных данных
            # В следующем шаге здесь будет реальная проверка сайта
            cur.execute(
                """
                INSERT INTO url_checks 
                (url_id, created_at) 
                VALUES (%s, %s)
                """,
                (id, created_at),
            )
            conn.commit()
            flash("Страница успешно проверена", "success")

    return redirect(url_for("show_url", id=id))


if __name__ == "__main__":
    app.run(debug=True)
