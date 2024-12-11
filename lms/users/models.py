from django.contrib.auth.models import AbstractUser
from django.db import models
from materials.models import Lesson, Course


class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name='почта', unique=True)
    phone_number = models.CharField(max_length=20)
    city = models.CharField(max_length=30)
    avatar = models.ImageField(upload_to='images', null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [email]


class Payments(models.Model):
    class SubjectType(models.TextChoices):
        LESSON = "lesson"
        COURSE = "course"

    class PayMethod(models.TextChoices):
        TRANSFER = "transfer"
        CASH = "cash"

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    date = models.DateTimeField(null=False)
    subject = models.CharField(max_length=6, choices=SubjectType.choices)
    amount = models.IntegerField()
    pay_method = models.CharField(max_length=8, choices=PayMethod.choices)
    lesson = models.ForeignKey(Lesson, on_delete=models.PROTECT, null=True)
    course = models.ForeignKey(Course, on_delete=models.PROTECT, null=True)
