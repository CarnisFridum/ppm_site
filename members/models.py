from django.db import models
from django.contrib.auth.models import User

class ProfilePic(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to="images/user_pic")

    def __str__(self):
        return "@{}".format(self.user)