# 🔍 Page Analyzer

![Hexlet tests](https://github.com/IDarhanI/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)
![Build](https://github.com/IDarhanI/python-project-83/actions/workflows/build.yml/badge.svg)
![Lint](https://github.com/IDarhanI/python-project-83/actions/workflows/lint.yaml/badge.svg)
![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=IDarhanI_python-project-83&metric=alert_status)
![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=IDarhanI_python-project-83&metric=sqale_rating)

Веб-приложение для анализа веб-страниц на SEO-пригодность. Проверяет доступность страниц, извлекает ключевые метаданные и отслеживает изменения.

## 🌐 Демо

Приложение развернуто на Render: [https://python-project-83-4utz.onrender.com/](https://python-project-83-4utz.onrender.com/)

## ✨ Возможности

- **Валидация URL** – проверка корректности и уникальности URL-адресов
- **Проверка доступности** – анализ HTTP статус-кодов ответов
- **SEO-анализ** – извлечение ключевых метаданных:
  - Заголовок страницы (`<title>`)
  - Основной заголовок (`<h1>`)
  - Мета-описание (`<meta name="description">`)
- **История проверок** – хранение и отображение результатов всех проверок
- **Адаптивный интерфейс** – современный дизайн на Bootstrap 5

## 🏗️ Архитектура

- **Backend**: Flask (Python)
- **База данных**: PostgreSQL
- **Frontend**: Jinja2, Bootstrap 5
- **Анализ HTML**: BeautifulSoup4
- **Валидация**: validators, requests
- **CI/CD**: GitHub Actions, SonarQube

## 📦 Установка и запуск

### Предварительные требования

- Python 3.9+
- PostgreSQL 12+
- Git
- [uv](https://github.com/astral-sh/uv) (установится автоматически)

### Локальная установка

```bash
# 1. Клонировать репозиторий
git clone https://github.com/IDarhanI/python-project-83.git
cd python-project-83

# 2. Установить зависимости
make install

# 3. Создать базу данных
createdb page_analyzer

# 4. Применить миграции
psql -d $DATABASE_URL -f database.sql

# 5. Запустить приложение в режиме разработки
make dev