import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webserver_prj.settings')
django.setup()

<<<<<<< HEAD
from blog.models import Post

Post.objects.all().delete()
=======
from main.models import car_list

car_list.objects.all().delete()
>>>>>>> origin/New-main
