# QRKot
Приложение собирает пожертвования в воображаемый фонд QRKot на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.

В Фонде QRKot может быть открыто несколько целевых проектов. У каждого проекта есть название, описание и сумма, которую планируется собрать. После того, как нужная сумма собрана — проект закрывается.
Пожертвования в проекты поступают по принципу First In, First Out: все пожертвования идут в проект, открытый раньше других; когда этот проект набирает необходимую сумму и закрывается — пожертвования начинают поступать в следующий проект.

## Технологии
Проект реализован на современном асинхронном стеке FastAPI + SQLAlchemy с использованием аутентификации через FastAPI Users. Для работы с базой данных применяется SQLite с асинхронным драйвером aiosqlite и системой миграций Alembic. Сервер запускается через ASGI-сервер Uvicorn. Тестирование проводится с помощью pytest с поддержкой асинхронных вызовов.

- python 3.9

Backend Framework:
- FastAPI (v0.78.0) - основной фреймворк для API
- Starlette (v0.19.1) - лежит в основе FastAPI
- Uvicorn (v0.17.6) - ASGI-сервер для запуска

База данных:
- SQLAlchemy (v1.4.36) - ORM для работы с БД
- Alembic (v1.7.7) - система миграций
- aiosqlite (v0.17.0) - асинхронный драйвер для SQLite

Аутентификация/Пользователи:
- FastAPI Users (v10.0.4) - система аутентификации
- JWT (PyJWT v2.3.0) - токены для авторизации

Тестирование:
- Pytest (v7.1.3) + pytest-asyncio (v0.23.4)

Валидация данных:
- Pydantic (v1.9.1) - валидация моделей

Отчёт в Google Sheets через API:
- Google Sheets API (v4) - отчёт
- Aiogoogle (v4.2.0) - асинхронный клиент для Google API

## Установка
Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Valerii-Khodorishchenko/cat_charity_fund
cd cat_charity_fund
```
Создать и заполнить файл `.env` переменными окружения

```bash
touch .env
# Подключение базы данных
echo "DATABASE_URL=sqlite+aiosqlite:///./fastapi.db" >> .env
# Добавление секретного ключа
echo "SECRET=$(python -c 'import secrets; print(secrets.token_urlsafe(32))')" >> .env

# Опционально:
# Создать суперпользователя при первом запуске
# Укажите собственные FIRST_SUPERUSER_EMAIL и FIRST_SUPERUSER_PASSWORD
echo "FIRST_SUPERUSER_EMAIL=root@admin.ru" >> .env
echo "FIRST_SUPERUSER_PASSWORD=root" >> .env
```

Cоздать и активировать виртуальное окружение:

* Если у вас Linux/macOS

    ```
    python3.9 -m venv venv
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    py -3.9 -m venv venv
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip

pip install -r requirements.txt
```
## Запуск
### Подготовка базы данных к запуску
Необходимо выполнить только при первом запуске. Сама база данных по умолчанию будет создана в корне проекта`fastapi.db`
```bash
alembic upgrade head
```
Для того чтобы запустить сервис в первый и последующие разы используйте

```bash
uvicorn app.main:app
```
## Подключение отчёта в Google Sheets

### Создать проект для работы с API платформы Google Cloud
[Перейдите на консоль разработчика](https://console.cloud.google.com/projectselector2/home/dashboard) (дашборд) → Нажмите кнопку `Create Project` → Задайте имя проекту → Нажмите кнопку `Create`

### Подключить Google Drive API и Google Sheets API к созданному проекту
- На плитке `APIs` нажмите `Go to APIs` overview.
- Нажмите `Enabled APIs and services` или выберите в меню слева пункт `Library`.
- В открывшемся окне выберите по очереди Google Drive API и Google Sheets API.
- Создайте сервисный аккаунт:
    - Перейдите в раздел `Credentials`.
    - Нажмите `Create credentials` и выберите пункт `Service account`.
    - Заполните поля `Service account name, Service account ID, Service account description`.
    - Выберите роль для сервисного аккаунта.
    - Назначьте права администратора вашему пользовательскому аккаунту.
### Получить JSON-файл с ключом доступа к сервисному аккаунту
Перейдите на экран `Credentials/<название вашего сервисного аккаунта>` → Нажмите `Keys` → `Add Key` → `Create New Key` → Выберите формат JSON → Нажмите `Create`
### Добавить ключ и email Google-аккаунта в переменные окружения
- Сохраните `JSON-файл` в корне проекта как `key.json`. Этот файл с чувствительными данными не будет индексироваться в git репозитории проекта.
- Добавьте ключ в переменные окружения:
```bash
python3 json_to_env.py
```
- Добавьте email Google-аккаунта в переменные окружения:
```bash
echo "email=<адрес_вашего_Google-аккаунта>" >> .env
```

## Примеры запросов к API
С примерами запросов можно ознакомиться после запуска проект по **ссылкам**:

[![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white)](http://127.0.0.1:8000/docs/)
[![ReDoc](https://img.shields.io/badge/-ReDoc-%23000000?style=for-the-badge&logo=read-the-docs&logoColor=white)](http://127.0.0.1:8000/redoc/)


## Контакты
**Автор:** [Ходорищенко Валерий (Khodorishchenko Valeriy)](https://github.com/Valerii-Khodorishchenko)

[![GitHub](https://img.shields.io/badge/GitHub-%23000000?style=flat&logo=github&logoColor=white)](https://github.com/Valerii-Khodorishchenko)
[![Telegram](https://img.shields.io/badge/Telegram-%2300A9E0?style=flat&logo=telegram&logoColor=white)](https://t.me/KhodorishchenkoValerii)