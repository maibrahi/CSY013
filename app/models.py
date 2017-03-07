from django.db import models

from social_django.models import AbstractUserSocialAuth, DjangoStorage, USER_MODEL
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

class CustomUserSocialAuth(AbstractUserSocialAuth):
    user = models.ForeignKey(USER_MODEL, related_name='custom_social_auth',
                             on_delete=models.CASCADE)


class CustomDjangoStorage(DjangoStorage):
    user = CustomUserSocialAuth



class Module(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=200)
    name = models.CharField(max_length=200)

    def get_students(self):
        return Student.objects.filter(module_ids__contains=[self.id])

    def __str__(self):
        return self.name

class Student(models.Model):
    module_ids = ArrayField(models.IntegerField())
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

    def name(self):
        return self.first_name + " " + self.last_name

    def get_modules(self):
        return Module.objects.filter(id__in=self.module_ids)
