import os


import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()
from django.core.exceptions import ValidationError
from main_app.models import VideoGame, Invoice, BillingInfo, Technology, Project, Programmer, Task, Exercise
from django.db.models import Sum, Count
from datetime import date
# Create task instances with custom creation dates

