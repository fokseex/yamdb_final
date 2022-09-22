# API сервис рекомендаций
![yamdb workflow](https://github.com/fokseex/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg )
Проект собирает отзывы (Review) пользователей на произведения (Title).<br>  
Произведения делятся на категории: "Книги", "Фильмы", "Музыка". Список категорий (Category) может быть расширен.<br>  
Сами произведения не хранятся, здесь нельзя посмотреть фильм или послушать музыку.<br>  
В каждой категории есть произведения: книги, фильмы или музыка. Произведению может быть присвоен жанр из списка предустановленных.<br>  
Новые жанры может создавать только администратор.<br>  
Благодарные или возмущённые читатели оставляют к произведениям текстовые отзывы (Review) и выставляют произведению рейтинг.<br>  
## Используемые технологии:
>- Python 3.8.13
>- Django==3.2.15
>- PostgreSQL
>- PyJWT==2.4.0
>- djangorestframework==3.13.1
>- django-filter==22.1

## Ресурсы API YaMDb<br>  
**auth**: аутентификация.<br>  
  
**users**: пользователи.<br>  
  
**titles**: произведения, к которым пишут отзывы (определённый фильм, книга или песенка).<br>  
  
**categories**: категории (типы) произведений ("Фильмы", "Книги", "Музыка").<br>  
  
**genres**: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.<br>  
  
**reviews**: отзывы на произведения. Отзыв привязан к определённому произведению.<br>  
  
**comments**: комментарии к отзывам. Комментарий привязан к определённому отзыву.<br>  
  
## Алгоритм регистрации пользователей<br>  
Пользователь отправляет POST-запрос с параметрами email и username на `/api/v1/auth/signup/`.<br>  
Сервис YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на указанный адрес email.<br>  
Пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт `/api/v1/auth/token/`, в ответе на запрос ему приходит token (JWT-токен)<br>  
После регистрации и получения токена пользователь может отправить PATCH-запрос на эндпоинт `/api/v1/users/me/` и заполнить поля в своём профайле<br>  
  
## Пользовательские роли<br>  
**Аноним** — может просматривать описания произведений, читать отзывы и комментарии.<br>  
  
**Аутентифицированный пользователь (user)** — может читать всё, как и Аноним, дополнительно может публиковать отзывы и ставить рейтинг произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы и ставить им оценки; может редактировать и удалять свои отзывы и комментарии, редактировать свои оценки произведений.<br>  
  
**Модератор (moderator)** — те же права, что и у Аутентифицированного пользователя плюс право удалять и редактировать любые отзывы и комментарии.<br>  
  
**Администратор (admin)** — полные права на управление проектом и всем его содержимым. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.<br>  
 
**Суперюзер Django** — те же права, что и у роли Администратор.<br>  
  
## Установка<br>  
 ***Склонируйте репозиторий***:
``` bash
git clone git@github.com:fokseex/infra_sp2.git  
```
***Создайте .env файл в папке /infra. Измените значения DB_NAME, 
POSTGRES_USER, POSTGRES_PASSWORD***:
``` bash
DB_ENGINE=django.db.backends.postgresql
DB_NAME=DB_NAME
POSTGRES_USER=POSTGRES_USERNAME
POSTGRES_PASSWORD=DB_PASSWORD
DB_HOST=db
DB_PORT=5432
``` 
***Из папки /infra запустите команду***: 
``` bash
docker-compose up
``` 
***Выполните по очереди команды:***:
``` bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input
```
***Загрузите тестовые данные из csv файлов:*** 
```bash
docker-compose exec web python manage.py parser_csv
```

Проект запущен и доступен по адресу [localhost](http://localhost)
  
Документация API YaMDb доступна по адрес [http://localhost/redoc/](http://localhost/redoc/)

## Примеры запросов и ответов

- *api/v1/signup/* - регистрация нового пользователя
```json
{
  "email": "string",
  "username": "string"
}
```
- *api/v1/token/* - получить токен (используйте код из почты)
```json
{
  "username": "string",
  "confirmation_code": "string"
}
```
- *api/v1/categories/* - категории произведений
```json
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "name": "string",
        "slug": "string"
      }
    ]
  }
]
```
- *api/v1/genres/* - Жанры произведений
```json
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "name": "string",
        "slug": "string"
      }
    ]
  }
]
```
- *api/v1/titles/* - Произведения
```json
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "name": "string",
        "year": 0,
        "rating": 0,
        "description": "string",
        "genre": [
          {
            "name": "string",
            "slug": "string"
          }
        ],
        "category": {
          "name": "string",
          "slug": "string"
        }
      }
    ]
  }
]
```
- *api/v1/titles/{title_id}/reviews/* - Отзывы на произведения
```json
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "text": "string",
        "author": "string",
        "score": 1,
        "pub_date": "2022-06-29T18:15:22Z"
      }
    ]
  }
]
```
- *api/v1/titles/{title_id}/reviews/{rewiew_id}/comments/* - Комментарии к отзывам
```json
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "text": "string",
        "author": "string",
        "pub_date": "2022-06-29T18:15:22Z"
      }
    ]
  }
]
```
- *api/v1/users/* - Управление пользователями
```json
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "username": "string",
        "email": "user@example.com",
        "first_name": "string",
        "last_name": "string",
        "bio": "string",
        "role": "user"
      }
    ]
  }
]
```
- *api/v1/users/me/* - Управление своей учетной записью
```json
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```