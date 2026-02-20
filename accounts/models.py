from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('TEAMLEAD', 'Team Lead'),
        ('EMPLOYEE', 'Employee'),
    ]
    DEPARTMENT_CHOICES = [
        ('DIGITAL', 'Digital'),
        ('AERONAUTIQUE', 'Aeronautique'),
        ('AUTOMOBILE', 'Automobile'),
        ('QUALITE', 'Qualite'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='EMPLOYEE')
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES, default='DIGITAL')
    keycloak_id = models.CharField(max_length=64, blank=True, null=True)

    # No duplicate groups/user_permissions fields; inherited from AbstractUser
