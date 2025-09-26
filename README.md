# Backend-test-task-fastapi

Тестовое задание на вакансию Backend-разработчик (Python FastAPI)

---

## Стек технологий
- Python 3.12
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- Docker + docker-compose
- Pytest + HTTPX (тестирование)

---

## Запуск проекта

### 1. Клонирование репозитория

### 2. Настройка окружения

Создайте `.env` в корне проекта:
- Строка подключения к БД
- Секретный ключ для хеширования
- Количество минут жизни access_token
- Количество дней жизни refresh_token
- Секретный ключ для получения роли админа

```env
DATABASE_URL=postgresql+asyncpg://user:password@host:5432/db
SECRET_KEY=supersecret
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
ADMIN_KEY = ADMIN
```

### 3. Запуск через Docker

```bash
docker-compose up -d --build
```

**В случае возникновения следующей ошибки (обычно для Windows):**
```
/app/startup.sh: no such file or directory
```

**Нужно убедится, что все текстовые файлы (например, startup.sh) сохранены с индикатором конца строки LF (Line Feed), или иметь настройку: 
```git config --global core.autocrlf true```**

После запуска документация Swagger доступна по адресу /docs

---
## Список эндпоинтов

### Авторизация

* `POST /api/v1/auth/register` — регистрация (email, password, admin_key) 
* `POST /api/v1/auth/login` — логин (email, password)

**login возвращает access_token, который затем используется для идентификации пользователя в остальных эндпоинтах**

* `POST /api/v1/auth/refresh` — обновление токена
* `GET /api/v1/users/me` — данные текущего пользователя

Роли:

* `USER` — базовый доступ
* `ADMIN` — доступ к CRUD для категорий и постов, управление ролями, для её получения при регистрации нужно указать секретный ключ администратора (admin_key)


### Публичные

* `GET /api/v1/posts` — список постов
* `GET /api/v1/posts/{slug}` — пост по slug
* `GET /api/v1/categories` — список категорий
* `GET /api/v1/categories/{slug}/posts` — посты категории
* `GET /api/v1/me` — информация о текущем пользователе

### Админские

Категории:
* `POST /api/v1/admin/create_category` — создать категорию
* `PATCH /api/v1/admin/update_category/{slug}` — изменить категорию
* `DELETE /api/v1/admin/delete_category/{slug}` — удалить категорию

Посты:
* `POST /api/v1/admin/post` — создать пост
* `PATCH /api/v1/admin/update_post/{slug}` — изменить пост
* `DELETE /api/v1/admin/delete_post/{slug}` — удалить пост

**При создании и редактировании постов добавлена сантитаризация HTML через Bleach**

Пользователи:
* `GET /api/v1/admin/users` — получить список пользователей
* `PATCH /api/v1/admin/update_user_role/{user_id}` — изменить роль пользователя

---

## Тесты

Для демонстрации сделан один простой автоматический тест на создание пользователя в директории tests

Использован pytest + httpx

---

