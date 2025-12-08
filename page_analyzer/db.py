import os

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import DictCursor

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is not set in environment variables")
    return psycopg2.connect(DATABASE_URL)


def get_url_by_id(url_id):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT * FROM urls WHERE id = %s", (url_id,))
            result = cursor.fetchone()
            if result:
                return dict(result)
            return None


def get_url_by_name(url_name):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT * FROM urls WHERE name = %s", (url_name,))
            result = cursor.fetchone()
            if result:
                return dict(result)
            return None


def get_all_urls():
    with get_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("""
                SELECT 
                    urls.id,
                    urls.name,
                    urls.created_at,
                    MAX(url_checks.created_at) as last_check_date,
                    MAX(url_checks.status_code) as last_status_code
                FROM urls
                LEFT JOIN url_checks ON urls.id = url_checks.url_id
                GROUP BY urls.id, urls.name, urls.created_at
                ORDER BY urls.created_at DESC
            """)
            results = cursor.fetchall()
            return [dict(row) for row in results]


def add_url(url_name):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                "INSERT INTO urls (name) VALUES (%s) RETURNING id", (url_name,)
            )
            url_id = cursor.fetchone()["id"]
            conn.commit()
            return url_id


def get_url_checks(url_id):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                """
                SELECT id, status_code, h1, title, description, created_at
                FROM url_checks
                WHERE url_id = %s
                ORDER BY created_at DESC
                """,
                (url_id,),
            )
            results = cursor.fetchall()
            return [dict(row) for row in results]


def add_url_check(url_id):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO url_checks (url_id)
                VALUES (%s)
                RETURNING id, created_at
                """,
                (url_id,),
            )
            result = cursor.fetchone()
            conn.commit()
            return dict(result) if result else None


def add_url_check_with_data(url_id, check_data):
    """
    Добавляет проверку сайта с данными.
    check_data должен быть словарем с ключами:
    - status_code (int)
    - h1 (str, optional)
    - title (str, optional)
    - description (str, optional)
    """
    with get_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO url_checks 
                (url_id, status_code, h1, title, description)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id, created_at
                """,
                (
                    url_id,
                    check_data.get("status_code"),
                    check_data.get("h1", "")[
                        :255
                    ],  # Ограничиваем длину как в базе
                    check_data.get("title", "")[:255],
                    check_data.get("description", ""),
                ),
            )
            result = cursor.fetchone()
            conn.commit()
            return dict(result) if result else None
