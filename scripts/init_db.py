import django
django.setup()

from django.contrib.auth.models import User

from flashcards.models import Bin

"""
Create some initial data 
"""

users = User.objects.all()

if not users:

    print ("Creating superuser admin/admin...")
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')

    # pre-create bins if new database
    # 5 seconds, 25 seconds, 2 minutes, 10 minutes, 1 hour, 5 hours, 1 day, 5 days, 25 days, 4 months, and never.
    # 0 and 11 are special, as amount and unit are not used

    Bin(order=0, amount=0, unit='seconds').save()
    Bin(order=1, amount=5, unit='seconds').save()
    Bin(order=2, amount=25, unit='seconds').save()
    Bin(order=3, amount=2, unit='minutes').save()
    Bin(order=4, amount=10, unit='minutes').save()
    Bin(order=5, amount=1, unit='hours').save()
    Bin(order=6, amount=5, unit='hours').save()
    Bin(order=7, amount=1, unit='days').save()
    Bin(order=8, amount=5, unit='days').save()
    Bin(order=9, amount=25, unit='days').save()
    Bin(order=10, amount=4, unit='months').save()
    Bin(order=11, amount=12, unit='months').save()


else:
    print ("Already data in db. Skipping ...")

