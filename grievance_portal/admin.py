from django.contrib import admin
from .models import Complaint, Query, Student

# Register your models here.
admin.site.register(Student)
admin.site.register(Complaint)
admin.site.register(Query)
