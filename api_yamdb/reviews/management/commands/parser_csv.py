import csv

from django.core.management.base import BaseCommand
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class Command(BaseCommand):
    help = 'Заливка csv прайсов'

    def handle(self, *args, **options):
        # Парсинг категорий
        with open('static/data/category.csv', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                category = Category(id=row[0],
                                    name=row[1],
                                    slug=row[2]
                                    )
                category.save()

        # Парсинг жанров
        with open('static/data/genre.csv', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                genre = Genre(id=row[0],
                              name=row[1],
                              slug=row[2]
                              )
                genre.save()

        # Парсинг пользователей
        with open('static/data/users.csv', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                user = User(id=row[0],
                            username=row[1],
                            email=row[2],
                            role=row[3]
                            )
                user.save()

        # Парсинг произведений
        with open('static/data/titles.csv', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                title = Title(id=row[0],
                              name=row[1],
                              year=row[2],
                              category_id=row[3]
                              )
                title.save()

        # Парсинг отзывов
        with open('static/data/review.csv', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                review = Review(id=row[0],
                                title_id=row[1],
                                text=row[2],
                                author_id=row[3],
                                score=row[4],
                                pub_date=row[5]
                                )
                review.save()

        # Парсинг комментариев
        with open('static/data/comments.csv', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                comment = Comment(id=row[0],
                                  review_id=row[1],
                                  text=row[2],
                                  author_id=row[3],
                                  pub_date=row[4]
                                  )
                comment.save()

        # Парсинг связки жанры - произведения
        with open('static/data/genre_title.csv', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                title = Title.objects.get(id=row[1])
                title.genre.add(row[2])
                title.save()

        print('Все файлы залиты')
