import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kittygram2.settings')
django.setup()

from django.contrib.auth import get_user_model
from cats.models import Cat, Trip, TripStop

User = get_user_model()

# Get existing superuser
user = User.objects.filter(is_superuser=True).first()

if not user:
    print('ERROR: No superuser found!')
    print('Please create a superuser first:')
    print('  python manage.py createsuperuser')
    exit()

# Create cats if they don't exist
if Cat.objects.count() < 3:
    Cat.objects.all().delete()
    cats = [
        Cat.objects.create(
            name='Barsik',
            color='Black',
            birth_year=2020,
            owner=user
        ),
        Cat.objects.create(
            name='Murzik',
            color='Ginger',
            birth_year=2019,
            owner=user
        ),
        Cat.objects.create(
            name='Snezok',
            color='White',
            birth_year=2021,
            owner=user
        ),
    ]
else:
    cats = list(Cat.objects.all())

# Create trips
if not Trip.objects.exists():
    today = datetime.now().date()

    trip1 = Trip.objects.create(
        title='Europe Tour',
        description='Long journey through European capitals',
        cat=cats[0],
        owner=user,
        start_date=today - timedelta(days=30),
        end_date=today + timedelta(days=10),
        status='active'
    )

    trip2 = Trip.objects.create(
        title='Beach Vacation',
        description='Summer vacation on Baltic Sea',
        cat=cats[1],
        owner=user,
        start_date=today + timedelta(days=5),
        end_date=today + timedelta(days=20),
        status='planned'
    )

    trip3 = Trip.objects.create(
        title='Mountain Adventure',
        description='Alpine journey through Switzerland',
        cat=cats[2],
        owner=user,
        start_date=today - timedelta(days=60),
        end_date=today - timedelta(days=30),
        status='completed'
    )

    # Create stops for trip1
    TripStop.objects.create(
        trip=trip1,
        location_name='Berlin, Germany',
        visit_date=today - timedelta(days=30),
        notes='Museums and galleries',
        order=1
    )

    TripStop.objects.create(
        trip=trip1,
        location_name='Prague, Czech Republic',
        visit_date=today - timedelta(days=20),
        notes='Beautiful medieval streets',
        order=2
    )

    TripStop.objects.create(
        trip=trip1,
        location_name='Vienna, Austria',
        visit_date=today - timedelta(days=10),
        notes='Palaces and classical music concerts',
        order=3
    )

    # Create stops for trip2
    TripStop.objects.create(
        trip=trip2,
        location_name='Tallinn, Estonia',
        visit_date=today + timedelta(days=5),
        notes='Walk through old town',
        order=1
    )

    TripStop.objects.create(
        trip=trip2,
        location_name='Riga, Latvia',
        visit_date=today + timedelta(days=12),
        notes='Beaches and entertainment',
        order=2
    )

    # Create stops for trip3
    TripStop.objects.create(
        trip=trip3,
        location_name='Zurich, Switzerland',
        visit_date=today - timedelta(days=60),
        notes='Alpine lakes and mountains',
        order=1
    )

    TripStop.objects.create(
        trip=trip3,
        location_name='Interlaken, Switzerland',
        visit_date=today - timedelta(days=45),
        notes='Alpine peaks and trails',
        order=2
    )

    TripStop.objects.create(
        trip=trip3,
        location_name='Geneva, Switzerland',
        visit_date=today - timedelta(days=30),
        notes='Majestic city on the lake',
        order=3
    )

    print('[OK] Test data created:')
    print(f'  - {len(cats)} cats')
    print(f'  - 3 trips')
    print(f'  - 8 trip stops')
else:
    print('[WARN] Data already exists')
