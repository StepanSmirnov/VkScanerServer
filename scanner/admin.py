from django.contrib import admin
from .models import Person
from .models import Photo

admin.site.register(Person)
admin.site.register(Photo)
# Register your models here.
