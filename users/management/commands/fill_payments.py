from django.core.management import BaseCommand
from users.models import Payments, User
from materials.models import Lesson, Course
import random
import datetime

class Command(BaseCommand):
    def handle(self, *args, **options):
        User.objects.create(email="user3@mail.ru", phone_number="+796678", city="Moscow", password='lms12345')
        User.objects.create(email="user4@mail.ru", phone_number="+796665", city="St. Peterburg", password='lms12345')
        users = User.objects.all()
        Course.objects.create(name="Python")
        Course.objects.create(name="Java")
        courses = Course.objects.all()
        for i in range(10):
            Payments.objects.create(user=random.choice(users), date=datetime.datetime.now().date(),
                                    subject=Payments.SubjectType.COURSE, amount=random.randint(10000, 20000),
                                    pay_method=random.choice(["transfer", "cash"]), course=random.choice(courses))
