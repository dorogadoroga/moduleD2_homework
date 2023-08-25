from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category

class Command(BaseCommand):
    help = 'Delete all posts in chosen category'

    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument('category_slug', nargs='+', type=str)

    def handle(self, *args, **options):
        cat_list = []
        for arg in args:
            cat = Category.objects.get(slug=arg)
            if cat not in Category.objects.all():
                self.stdout.write(f'Category {arg} not found')
                return
            else:
                cat_list.append(cat)
        self.stdout.write(f'Do you really want to delete all posts in {args}? yes/no')
        answer = input()
        if answer == 'y' or answer == 'yes':
            for cat in cat_list:
                Post.objects.filter(category=cat).delete()
                self.stdout.write(self.style.SUCCESS(f'Succesfilly deleted posts in {cat.slug}'))

    # def handle(self, *args, **options):
    #     answer = input(f'Вы правда хотите удалить все статьи в категории {options["category"]}? yes/no')
    #
    #     if answer != 'yes':
    #         self.stdout.write(self.style.ERROR('Отменено'))
    #
    #     try:
    #         category = Category.get(name=options['category'])
    #         Post.objects.filter(category == category).delete()
    #         self.stdout.write(self.style.SUCCESS(
    #             f'Succesfully deleted all news from category {category.name}'))  # в случае неправильного подтверждения говорим, что в доступе отказано
    #     except Post.DoesNotExist:
    #         self.stdout.write(self.style.ERROR(f'Could not find category {}'))