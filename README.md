# 🔍 Page Analyzer

[![Hexlet tests](https://github.com/IDarhanI/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/IDarhanI/python-project-83/actions/workflows/hexlet-check.yml)
[![Build](https://github.com/IDarhanI/python-project-83/actions/workflows/build.yml/badge.svg)](https://github.com/IDarhanI/python-project-83/actions/workflows/build.yml)
[![Lint](https://github.com/IDarhanI/python-project-83/actions/workflows/lint.yaml/badge.svg)](https://github.com/IDarhanI/python-project-83/actions/workflows/lint.yaml)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=IDarhanI_python-project-83&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=IDarhanI_python-project-83)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=IDarhanI_python-project-83&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=IDarhanI_python-project-83)

Веб-приложение для анализа веб-страниц на SEO-пригодность. Проверяет доступность страниц, извлекает ключевые метаданные и отслеживает изменения.


🚀 **Приложение развернуто на Render:** [https://python-project-83-4utz.onrender.com/](https://python-project-83-4utz.onrender.com/)

## 📋 Функциональность

### Основные возможности:
- ✅ **Добавление сайтов** – введите URL для анализа
- ✅ **SEO-анализ** – проверка ключевых метаданных страницы
- ✅ **Мониторинг доступности** – отслеживание кодов ответа сервера
- ✅ **История проверок** – просмотр всех предыдущих проверок
- ✅ **Валидация URL** – проверка корректности введенных адресов

### Что анализируется:
- **Код ответа HTTP** – статус доступности страницы (200, 404, 500 и т.д.)
- **Заголовок H1** – основной заголовок страницы
- **Тег Title** – заголовок страницы для браузера и поисковых систем
- **Мета-описание** – описание страницы для поисковых систем

## 🛠 Технологии

## 🚀 Быстрый старт

### Предварительные требования:
- Python 3.11 или выше
- PostgreSQL 14+
- Git

### Локальная установка:

1. **Клонируйте репозиторий:**
```bash
git clone https://github.com/IDarhanI/python-project-83.git
cd python-project-83
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