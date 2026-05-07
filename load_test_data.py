import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kittygram2.settings')
django.setup()

from django.contrib.auth import get_user_model
from cats.models import Cat, Achievement

User = get_user_model()

user = User.objects.filter(is_superuser=True).first()

if not user:
    print('Ошибка: суперпользователь не найден.')
    print('Сначала создайте его: python manage.py createsuperuser')
    exit(1)

ach1, _ = Achievement.objects.get_or_create(name='Ловкач')
ach2, _ = Achievement.objects.get_or_create(name='Чемпион')
ach3, _ = Achievement.objects.get_or_create(name='Красавец')

cat1, created = Cat.objects.get_or_create(
    name='Барсик', owner=user,
    defaults={'color': 'Black', 'birth_year': 2020}
)
if created:
    cat1.achievements.add(ach1, ach3)

cat2, created = Cat.objects.get_or_create(
    name='Мурзик', owner=user,
    defaults={'color': 'Ginger', 'birth_year': 2019}
)
if created:
    cat2.achievements.add(ach2)

cat3, created = Cat.objects.get_or_create(
    name='Снежок', owner=user,
    defaults={'color': 'White', 'birth_year': 2021}
)

print('[OK] Тестовые данные загружены:')
print(f'  - 3 кошки')
print(f'  - 3 достижения')
