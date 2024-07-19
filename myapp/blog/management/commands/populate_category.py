from typing import Any
from blog.models import Category
from django.core.management.base import BaseCommand



class Command(BaseCommand):
    help = "this command insert post data"
        
    def handle(self, *args: Any, **options: Any):
        #deleting existing categorydata
        Category.objects.all().delete()
        
        categories =['Sport','Technology','Science','Art','Food']
        
        for category_name in categories:
            Category.objects.create(name=category_name) 
       
        self.stdout.write(self.style.SUCCESS("COMPLETED INSERTING DATA!"))
        