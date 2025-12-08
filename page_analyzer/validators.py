from urllib.parse import urlparse

import validators


def normalize_url(url):
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"


def validate_url(url):
    if not url:
        return "URL обязателен"

    if len(url) > 255:
        return "URL превышает 255 символов"

    if not validators.url(url):
        return "Некорректный URL"

    return None
