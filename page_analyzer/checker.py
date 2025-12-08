import requests
from bs4 import BeautifulSoup


def check_website(url):
    """
    Проверяет сайт и возвращает информацию о нем.
    Возвращает словарь с информацией или None в случае ошибки.
    """
    try:
        # Устанавливаем таймауты для запроса
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Проверяем статус ответа

        # Парсим HTML с помощью BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # 1. Проверяем наличие тега <h1>
        h1_tag = soup.find("h1")
        h1_content = h1_tag.text.strip() if h1_tag else ""

        # 2. Проверяем наличие тега <title>
        title_tag = soup.find("title")
        title_content = title_tag.text.strip() if title_tag else ""

        # 3. Проверяем наличие тега <meta name="description">
        meta_desc = soup.find("meta", attrs={"name": "description"})
        description_content = (
            meta_desc.get("content", "").strip() if meta_desc else ""
        )

        return {
            "status_code": response.status_code,
            "h1": h1_content,
            "title": title_content,
            "description": description_content,
        }

    except requests.exceptions.RequestException:
        # Любая ошибка запроса (таймаут, соединение, HTTP ошибка и т.д.)
        return None
    except Exception:
        # Любая другая ошибка
        return None
