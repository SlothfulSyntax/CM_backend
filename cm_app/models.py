from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    contact_number = models.CharField(max_length=150, null=True, blank=True)
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]


class JobListing(models.Model):
    # Define the available job positions as choices
    POSITION_CHOICES = [
        ('Software Engineer', 'Software Engineer'),
        ('Software Developer', 'Software Developer'),
        ('Python Developer', 'Python Developer'),
        ('Java Developer', 'Java Developer'),
        ('MERN Stack Developer', 'MERN Stack Developer'),
        ('MEAN Stack Developer', 'MEAN Stack Developer'),
        ('Full Stack Developer', 'Full Stack Developer'),
        ('Data Analyst', 'Data Analyst'),
        ('Data Scientist', 'Data Scientist'),
        ('Data Engineer', 'Data Engineer'),
        ('Service Now Developer', 'Service Now Developer'),
        # Add more IT jobs here
    ]

    company_name = models.CharField(max_length=255)
    company_website = models.URLField(
        max_length=200,null=True, blank=True)  # Company website
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Salary
    location = models.CharField(max_length=255, default="India")  # Job location
    qualification = models.CharField(max_length=255, null=True, blank=True)  # Required qualifications
    experience = models.PositiveIntegerField(default=0)  # Years of experience
    batch = models.CharField(max_length=10,null=True, blank=True)  # Batch (optional)

    position = models.CharField(
        max_length=255, choices=POSITION_CHOICES, default='Software Engineer')  # Use choices here
    image = models.ImageField(upload_to='job_images/')
    description = models.TextField()
    apply_link = models.URLField(max_length=200)

    def __str__(self):
        return f"{self.company_name} - {self.get_position_display()}"
