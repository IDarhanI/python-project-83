import os
from datetime import datetime
from urllib.parse import urlparse

import psycopg2
import requests
import validators  # Добавляем для валидации URL
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")  # Добавили значение по умолчанию

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")


def is_valid_url(url):
    """Проверяет, является ли строка валидным URL."""
    if len(url) > 255:
        return False

    # Используем библиотеку validators для проверки
    if not validators.url(url):
        return False

    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def normalize_url(url):
    """Нормализует URL, оставляя только схему и домен."""
    parsed = urlparse(url)

    # Если нет схемы, добавляем https://
    if not parsed.scheme:
        url = "https://" + url
        parsed = urlparse(url)

    return f"{parsed.scheme}://{parsed.netloc}"


def get_connection():
    """Создает соединение с базой данных."""
    return psycopg2.connect(DATABASE_URL)


def parse_html(html_content):
    """
    Извлекает данные из HTML:
    - h1 (первый тег h1 на странице)
    - title (содержимое тега title)
    - description (content атрибут meta тега с name="description")
    """
    soup = BeautifulSoup(html_content, "html.parser")

    # Извлекаем h1
    h1_tag = soup.find("h1")
    h1 = h1_tag.get_text().strip() if h1_tag else None

    # Извлекаем title
    title_tag = soup.find("title")
    title = title_tag.get_text().strip() if title_tag else None

    # Извлекаем description
    meta_desc = soup.find("meta", attrs={"name": "description"})
    description = meta_desc.get("content", "").strip() if meta_desc else None

    return h1, title, description


@app.get("/")
def index():
    """Главная страница с формой добавления URL."""
    return render_template("index.html")


@app.post("/urls")
def add_url():
    """Добавление нового URL в базу данных."""
    url = request.form.get("url", "").strip()

    if not url:
        flash("URL обязателен", "danger")
        return render_template("index.html", url=url), 422

    if not is_valid_url(url):
        flash("Некорректный URL", "danger")
        return render_template("index.html", url=url), 422

    normalized_url = normalize_url(url)

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                # Проверяем, существует ли URL уже в базе
                cur.execute("SELECT id FROM urls WHERE name = %s", (normalized_url,))
                existing = cur.fetchone()

                if existing:
                    url_id = existing[0]
                    flash("Страница уже существует", "info")
                else:
                    # Создаем новую запись
                    created_at = datetime.now()
                    cur.execute(
                        "INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING id",
                        (normalized_url, created_at),
                    )
                    url_id = cur.fetchone()[0]
                    conn.commit()
                    flash("Страница успешно добавлена", "success")

        return redirect(url_for("url_show", id=url_id))

    except Exception as e:
        flash(f"Ошибка при сохранении: {str(e)}", "danger")
        return render_template("index.html", url=url), 500


@app.get("/urls")
def urls():
    """Страница со списком всех добавленных URL."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT 
                        urls.id, 
                        urls.name,
                        urls.created_at,
                        MAX(url_checks.created_at) as last_check_date,
                        (SELECT status_code 
                         FROM url_checks 
                         WHERE url_id = urls.id 
                         ORDER BY created_at DESC 
                         LIMIT 1) as last_check_status
                    FROM urls
                    LEFT JOIN url_checks ON urls.id = url_checks.url_id
                    GROUP BY urls.id, urls.name, urls.created_at
                    ORDER BY urls.created_at DESC
                """
                )
                urls_list = cur.fetchall()

        return render_template("urls_index.html", urls=urls_list)

    except Exception as e:
        flash(f"Ошибка при загрузке данных: {str(e)}", "danger")
        return render_template("urls_index.html", urls=[])


@app.get("/urls/<int:id>")
def url_show(id):
    """Страница с информацией о конкретном URL и его проверках."""
    try:
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

    except Exception as e:
        flash(f"Ошибка при загрузке данных: {str(e)}", "danger")
        return redirect(url_for("urls"))


@app.post("/urls/<int:id>/checks")
def url_check(id):
    """Запуск проверки конкретного URL."""
    try:
        # Получаем URL сайта из базы
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT name FROM urls WHERE id = %s", (id,))
                url_result = cur.fetchone()

                if not url_result:
                    flash("URL не найден", "danger")
                    return redirect(url_for("urls"))

                url_name = url_result[0]

        # Выполняем запрос к сайту с таймаутом
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

        response = requests.get(url_name, headers=headers, timeout=10)
        response.raise_for_status()  # Вызывает исключение для 4xx/5xx статусов

        # Извлекаем данные из HTML
        h1, title, description = parse_html(response.text)

        # Если description слишком длинный, обрезаем его
        if description and len(description) > 255:
            description = description[:252] + "..."

        # Создаем запись о проверке с извлеченными данными
        status_code = response.status_code
        created_at = datetime.now()

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO url_checks 
                    (url_id, status_code, h1, title, description, created_at) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (id, status_code, h1, title, description, created_at),
                )
                conn.commit()
                flash("Страница успешно проверена", "success")

    except requests.exceptions.RequestException as e:
        # Обработка всех исключений requests
        flash("Произошла ошибка при проверке", "danger")
        print(f"Request error: {e}")

    except Exception as e:
        flash(f"Ошибка при проверке: {str(e)}", "danger")
        print(f"Other error: {e}")

    return redirect(url_for("url_show", id=id))
