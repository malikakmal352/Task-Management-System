from django.contrib.auth.models import AbstractUser
from django.db import models

from auths.manager import UserManager


class User(AbstractUser):
    class Meta:
        db_table = "User"
        verbose_name_plural = "Users"
        managed = True
        ordering = ["date_joined"]

    username = models.CharField(max_length=150, null=True, unique=False)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    team_lead = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="team_parent",
    )
    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password"]

    def delete(self, using=None, keep_parents=False):
        super().delete()

    def save(self, *args, **kwargs):
        if not self.username:
            user_name = str(self.email.split("@")[0])
            self.username = user_name
            super().save(*args, **kwargs)
        super().save(*args, **kwargs)

    @staticmethod
    def create_user(email, password, username, **extra_fields):
        add_user = User(
            email=email,
            password=password,
            username=username,
            **extra_fields
        )
        add_user.set_password(password)
        add_user.save()
        return add_user

    def __str__(self):
        return self.username
