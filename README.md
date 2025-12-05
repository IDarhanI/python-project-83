### Hexlet tests and linter status:
[![Actions Status](https://github.com/IDarhanI/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/IDarhanI/python-project-83/actions)

# 🔍 Page Analyzer

[![Tests](https://github.com/your-username/python-project-83/actions/workflows/test.yml/badge.svg)](https://github.com/your-username/python-project-83/actions/workflows/test.yml)

Веб-приложение для анализа веб-страниц на SEO-пригодность. Проверяет доступность страниц, извлекает ключевые метаданные и отслеживает изменения.

## 🌐 Демо

Приложение развернуто на Render: [https://your-app-name.onrender.com](https://your-app-name.onrender.com)

## ✨ Возможности

- ✅ Добавление и валидация URL
- ✅ Проверка доступности страниц (HTTP статус коды)
- ✅ Извлечение SEO-метаданных:
  - Заголовок страницы (`<title>`)
  - Основной заголовок (`<h1>`)
  - Описание (`<meta name="description">`)
- ✅ История проверок для каждого сайта
- ✅ Адаптивный интерфейс на Bootstrap

## 🚀 Быстрый старт

### Установка

```bash
# Клонировать репозиторий
git clone https://github.com/your-username/python-project-83.git
cd python-project-83

# Установить зависимости
make install

# Создать базу данных
createdb page_analyzer
psql -d page_analyzer -f database.sql

# Запустить приложение
make dev