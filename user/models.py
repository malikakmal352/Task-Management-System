from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel

from auths.models import User

# Create your models here.


class Task(TimeStampedModel):
    class Meta:
        db_table = "Task"
        verbose_name_plural = "Tasks"
        managed = True
        ordering = ["-created"]

    class TaskStatus(models.TextChoices):
        pending = "pending", _("Pending")
        process = "process", _("In Process")
        review = "review", _("Review")
        change_request = "change_request", _("Change Request")
        complete = "complete", _("Complete")

    title = models.CharField(max_length=150)
    status = models.CharField(max_length=200, choices=TaskStatus.choices, blank=False, default=TaskStatus.pending)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="task_creator")
    assign_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assign_user", null=True, blank=True)
    deadline = models.DateTimeField()
    change_details = models.TextField(null=True, blank=True)
    description = models.TextField(default='')

    @staticmethod
    def create_task(title, creator, assign, deadline, description):
        try:
            assign_user = User.objects.get(id=assign)
            Task(
                title=title,
                creator=creator,
                deadline=deadline,
                assign_to=assign_user,
                description=description,
            ).save()
            return None
        except Exception as e:
            return e

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Team(TimeStampedModel):
    class Meta:
        db_table = "Team"
        verbose_name_plural = "Teams"
        managed = True
        ordering = ["-created"]

    team_title = models.CharField(max_length=150)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='team_creator')
    members = models.ManyToManyField(User, blank=True, related_name='team_members')

    @staticmethod
    def create_user_team(title, creator):
        add_team = Team(
            team_title=title,
            creator=creator
        ).save()
        return add_team

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.team_title
