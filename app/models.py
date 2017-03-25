from django.db import models

from social_django.models import AbstractUserSocialAuth, DjangoStorage, USER_MODEL
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

import time
from datetime import datetime, timedelta

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

    def __str__(self):
        return self.name()


class TimeSlot(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)

    ordered_student_ids = ArrayField(models.IntegerField())
    ordered_attendance = ArrayField(models.IntegerField())

    def __str__(self):
        return self.module.code + " " + self.printable_start()

    # def save(self, *args, **kwargs):
    #     if not self.end_time():
    #         self.end_time = self.get_default_end_time()
    #     super().save(*args, **kwargs)  # Call the "real" save() method.

    # default to 1 day from now
    # def get_default_end_time(self):
    #     return self.start_time() + timedelta(minutes=50)

    def printable_start(self):
        return self.start_time.strftime("%Y-%m-%d %H:%M")

    def printable_duration(self):
        delta = self.end_time - self.start_time
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        if hours > 0:
            if minutes > 0:
                return str(hours) + "hr" + str(minutes) + "min"
            else:
                return str(hours) + "hr"
        else:
            return str(minutes) + "min"

    def get_students(self):
        return Student.objects.filter(id__in=self.ordered_student_ids)

    def get_attendance(self):
        return sum(self.ordered_attendance) / len(self.ordered_attendance)

