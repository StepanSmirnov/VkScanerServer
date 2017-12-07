from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import admin
from django.utils.html import format_html

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    link = models.CharField(max_length=150, blank=True)
    access_token = models.CharField(max_length=150, blank=True)

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

class Person(models.Model):
    social_id = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    surname = models.CharField(max_length=250)
    timestamp = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return "{} {}".format(self.name, self.surname)

class Photo(models.Model):
    url = models.CharField(max_length=250)
    labels = models.TextField()
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    
class PhotoAdmin(admin.ModelAdmin):
    
    list_display = ('url', 'labels', 'person', 'image')    
    
    def image(self, obj):
        return format_html(
            '<img src="{}">',
            obj.url
        )

    image.admin_order_field = 'image'

    def __str__(self):
        return self.url
