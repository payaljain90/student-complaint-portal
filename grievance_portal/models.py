from datetime import datetime
from django.db import models

# Create your models here.
class Student(models.Model):
    prn = models.CharField(max_length=20, unique=True, primary_key=True)
    password = models.CharField(max_length=255)  
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15)
    department = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    admission_year = models.IntegerField()
    graduation_year = models.IntegerField()
    dob = models.DateField()
    gender = models.CharField(
        max_length=1,
        choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    )
    address = models.TextField()
    status = models.BooleanField(default=True) 

    

class Complaint(models.Model):
    COMPLAINT_CATEGORIES = [
        ('Academic', 'Academic'),
        ('Hostel', 'Hostel'),
        ('Mess', 'Mess'),
        ('Facilities', 'Facilities'),
        ('Faculties', 'Faculties'),
        ('Canteen', 'Canteen'),
        ('Others', 'Others'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Rejected', 'Rejected'),
    ]
    id = models.AutoField(primary_key=True)
    prn = models.ForeignKey(Student, to_field="prn", on_delete=models.CASCADE, null=True, blank=True)  # Link to Student using PRN
    complaint_type = models.CharField(max_length=50, choices=COMPLAINT_CATEGORIES)
    title = models.CharField(max_length=255)
    description = models.TextField()
    anonymous = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.id} - {self.title} - {self.prn if self.prn else 'Anonymous'}"
    


class Query(models.Model):
    QUERY_TYPES = [
        ("Bug/Error", "Bug/Error"),
        ("UI Issue", "UI Issue"),
        ("Login Issue", "Login Issue"),
        ("Feature Request", "Feature Request"),
        ("Other", "Other"),
    ]

    MODULES = [
        ("Login", "Login"),
        ("Dashboard", "Dashboard"),
        ("Complaint Management", "Complaint Management"),
        ("Profile", "Profile"),
        ("Other", "Other"),
    ]

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Resolved", "Resolved"),
    ]

    id = models.AutoField(primary_key=True)
    prn = models.ForeignKey(Student, to_field="prn", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField(blank=True, null=True)
    query_type = models.CharField(max_length=50, choices=QUERY_TYPES)
    module = models.CharField(max_length=50, choices=MODULES)
    evidence = models.ImageField(upload_to='query_evidence/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
            return f"{self.title} - {self.prn} - {self.status}"

    