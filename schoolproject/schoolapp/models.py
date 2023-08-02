from django.db import models

# Create your models here.
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Courses(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


purpose = (
    ("1", "Enquiry"),
    ("2", "Place Order"),
    ("3", "Return"),
    ("4", "Feedback"),
    ("5", "Queries"),
)

materials_choices = (
                    ('Notebook', 'Notebook'), 
                    ('Pen', 'Pen'),
                    ('Exam Papers', 'Exam Papers'),
                    ('Books', 'Books'))
gender_choices = (('M', 'Male'), ('F', 'Female'))

class Student(models.Model):
    first_name = models.CharField( max_length=50)
    last_name = models.CharField(max_length=100)
    dob = models.CharField(max_length=50)
    age = models.CharField(max_length=3)
    email = models.EmailField()
    address = models.TextField()
    phoneNumber = models.CharField(max_length=12)
    gender_choices = (('M', 'Male'), ('F', 'Female'))
    gender = models.CharField(max_length=1, choices=gender_choices)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, blank=True, null=True)
    courses = models.ForeignKey(Courses, on_delete=models.SET_NULL, blank=True, null=True)
    purpose = models.CharField(max_length=15,choices=purpose)
    materials_choices = (('Notebook', 'Notebook'), ('Pen', 'Pen'), ('Exam Papers', 'Exam Papers'),
                     ('Books', 'Books'), )
    materials = models.CharField(max_length=15,choices=materials_choices)
    def __str__(self):
        return self.first_name