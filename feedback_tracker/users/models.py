# define custom user model

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    def save(self, *args, **kwargs):
        # check if it is a new object and email is already in use
        if (
            not self.pk
            and self.email
            and User.objects.filter(email=self.email).exists()
        ):
            raise ValueError("Email already in use")
        return super().save(*args, **kwargs)
