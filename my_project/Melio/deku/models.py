from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


# Create your models here.
class Token(models.Model):
    user = models.OneToOneField(User, related_name="Token", on_delete=models.CASCADE)
    # related_name تستخدم للوصول إلى profile من خلال User كالتالي User.profile.filter()
    # عند حدف User يتم حدف Profile
    reset_password_token = models.CharField(max_length=50, null=True, blank=True)
    reset_password_expire = models.DateTimeField(null=True, blank=True)


@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    print("instance : ", instance)
    user = instance

    if created:
        profile = Token(user=user)
        profile.save()
