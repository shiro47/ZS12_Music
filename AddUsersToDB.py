import csv 
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "first_project.settings")
django.setup()

from django.contrib.auth.models import User



"""
csv_file=open('path\to\csv', encoding="utf-8")
"""

"""
CSV PATTERN: 
email;username;password
"""    
def add_users(csv_file):
    csv_file=csv.reader(csv_file, delimiter=";")
    
    for user_data in csv_file:
        email=user_data[0].replace('\ufeff', '')
        user = User.objects.create_user(username=user_data[1],
                                 email=email,
                                 password=user_data[2])
        user.save()
        
    return


#add_users(csv_file)