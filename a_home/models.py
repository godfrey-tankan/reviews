from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class SurveyAnswer(models.Model):
    question_id = models.IntegerField() 
    answer = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

class Question(models.Model):
    TEXT = 'text'
    MULTIPLE_CHOICE = 'multiple_choice'
    RATING_SCALE = 'rating'

    QUESTION_TYPES = [
        (TEXT, 'Text'),
        (MULTIPLE_CHOICE, 'Multiple Choice'),
        (RATING_SCALE, 'Rating Scale'),
    ]

    question_text = models.CharField(max_length=500)
    question_type = models.CharField(
        max_length=50,
        choices=QUESTION_TYPES,
        default=TEXT
    )
    is_required = models.BooleanField(default=True)  

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200) 

    def __str__(self):
        return self.choice_text

class DemographicData(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female')
    ]
    
    AGE_GROUP_CHOICES = [
        ('20_below', '20yrs and below'),
        ('21_30', '21-30yrs'),
        ('31_40', '31-40yrs'),
        ('41_50', '41-50yrs'),
        ('51_60', '51-60yrs')
    ]
    
    EXPERIENCE_CHOICES = [
        ('5_below', '5yrs and below'),
        ('6_9', '6-9yrs'),
        ('10_19', '10-19yrs'),
        ('20_above', '20 and above')
    ]
    
    QUALIFICATION_CHOICES = [
        ('below_o', 'Below O’ level'),
        ('o_level', 'O’ level'),
        ('a_level', 'A’ level'),
        ('diploma', 'Diploma'),
        ('undergraduate', 'Undergraduate'),
        ('postgraduate', 'Post-graduate')
    ]
    
    DESIGNATION_CHOICES = [
        ('senior_management', 'Senior Management'),
        ('professional_employees', 'Professional Employees'),
        ('middle_management', 'Middle Management'),
        ('line_employees', 'Line Employees')
    ]
    
    CONTRACT_CHOICES = [
        ('fixed_term', 'Fixed –Term Contract'),
        ('permanent', 'Permanent Contract')
    ]
    
    # Demographic Fields
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    age_group = models.CharField(max_length=10, choices=AGE_GROUP_CHOICES)
    work_experience = models.CharField(max_length=10, choices=EXPERIENCE_CHOICES)
    highest_qualification = models.CharField(max_length=20, choices=QUALIFICATION_CHOICES)
    designation = models.CharField(max_length=30, choices=DESIGNATION_CHOICES)
    department = models.CharField(max_length=100)  # Text input for department
    contract_type = models.CharField(max_length=15, choices=CONTRACT_CHOICES)

    def __str__(self):
        return f"{self.gender}, {self.age_group}, {self.designation}"



