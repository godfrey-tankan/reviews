from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class SurveyAnswer(models.Model):
    question_id = models.IntegerField()  # Assuming each question has an ID
    answer = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    # No ForeignKey to User for anonymity

