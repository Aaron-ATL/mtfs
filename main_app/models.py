from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .utils import send_activation_email
# Create your models here.

class Lesson(models.Model):
    number = models.IntegerField(default=1)
    title = models.CharField(max_length=200, default="Lesson X")
    description = models.TextField(default="Enter description")
    vimeo_id = models.CharField(max_length=50, default="000000000")
    length = models.IntegerField(default=5)  # rounded minutes
    thumbnail_id = models.IntegerField(default=100)
    lesson_file = models.CharField(max_length=60, default="lesson_file")

    def __str__(self):
        return f"{self.number}. {self.title}"

    class Meta:
        ordering = ["number"]


class Profile(models.Model):
    def default_progress_info():
        return {
            "completed_lessons":[]
        }
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    progress_info = models.JSONField(default=default_progress_info)
    
    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def send_invite(sender, instance, created, **kwargs):
    if created:
        send_activation_email(instance)
