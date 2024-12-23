from django.db import models
from django.conf import settings

class Course(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    preview = models.ImageField(upload_to='images', null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    preview = models.ImageField(upload_to='images', null=True)
    video_url = models.CharField(max_length=250)
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
