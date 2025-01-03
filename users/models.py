from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(verbose_name='почта', unique=True)
    phone_number = models.CharField(max_length=20, null=True)
    city = models.CharField(max_length=300, null=True)
    avatar = models.ImageField(upload_to='images', null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    @property
    def role(self):
        if self.groups.filter(name="moderators").exists():
            return "moderator"
        return "user"


class Payments(models.Model):
    from materials.models import Lesson, Course

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


class Subscription(models.Model):
    from materials.models import Course
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
