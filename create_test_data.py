"""Test data creation script. Last updated: 2026-05-05"""
from django.contrib.auth import get_user_model
from cats.models import Cat, Achievement

User = get_user_model()

# Create test users if they don't exist
user1, _ = User.objects.get_or_create(
    username='testuser1',
    defaults={'email': 'test1@example.com', 'first_name': 'Test', 'last_name': 'User1'}
)
user2, _ = User.objects.get_or_create(
    username='testuser2',
    defaults={'email': 'test2@example.com', 'first_name': 'Test', 'last_name': 'User2'}
)

# Set passwords
user1.set_password('testpass123')
user1.save()
user2.set_password('testpass123')
user2.save()

# Create achievements
ach1, _ = Achievement.objects.get_or_create(name='Ловкач')
ach2, _ = Achievement.objects.get_or_create(name='Чемпион')
ach3, _ = Achievement.objects.get_or_create(name='Красавец')

# Create test cats
cat1, _ = Cat.objects.get_or_create(
    name='Барсик',
    owner=user1,
    defaults={'color': 'Black', 'birth_year': 2020}
)
if cat1.achievements.count() == 0:
    cat1.achievements.add(ach1, ach3)

cat2, _ = Cat.objects.get_or_create(
    name='Мурзик',
    owner=user2,
    defaults={'color': 'Ginger', 'birth_year': 2019}
)
if cat2.achievements.count() == 0:
    cat2.achievements.add(ach2)

print("✓ Test data created successfully")
