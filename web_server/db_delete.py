import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webserver_prj.settings')
django.setup()

from blog.models import Post

Post.objects.all().delete()