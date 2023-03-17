from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUser(AbstractUser):
    user_type_data = (("admin", "admin"), ("user", "user"))
    user_type = models.CharField(default="admin", choices=user_type_data, max_length=10)


class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class Users(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    cantact_num = models.CharField(max_length=10)
    gender = models.CharField(max_length=10)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type=="admin":
            Admin.objects.create(admin=instance)
        if instance.user_type=="user":
            Users.objects.create(admin=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type=="admin":
        instance.admin.save()
    if instance.user_type=="user":
        instance.users.save()