from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

SECURITY_QUESTION_CHOICES = [
    ('q1', 'What is your favorite color?'),
    ('q2', 'What is the name of your first pet?'),
    ('q3', 'In which city were you born?'),
]

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name
class login_info(AbstractUser):
    username = models.CharField(max_length=255, unique = True)
    password = models.CharField(max_length=128)
    age = models.IntegerField(blank=True, default=0)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    security_question = models.CharField(max_length=255, choices=SECURITY_QUESTION_CHOICES, null=True, blank=True)
    security_answer = models.CharField(max_length=255, null=True, blank=True)
    # birth_date = models.DateField()


class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published", blank=True, default=timezone.now)

    def __str__(self):
        return self.question


class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="choices")
    name = models.CharField(max_length=255)
    voters = models.ManyToManyField(
        login_info, related_name="voted_options", blank=True, default=[]
    )

    @property
    def count(self):
        return self.voters.count()

    def __str__(self):
        return f"{self.name} - {self.count}"


# Explicitly declare app_label
class Meta:
    app_label = 'alpha'
