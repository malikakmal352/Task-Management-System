from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save

from auths.models import User
from user.models import Task, Team


def TaskDelete(task_id):
    try:
        query = Task.objects.get(id=task_id)
        query.delete()
        return ""
    except ObjectDoesNotExist as e:
        message = "Task with this id is not found"
        return None, message


def UpdateTask(task_title, assign_to_id, deadline, task_details, task_id):
    try:
        query = Task.objects.get(id=task_id)
        query.title = task_title
        query.deadline = deadline
        query.description = task_details
        if assign_to_id:
            assign_to = User.objects.get(id=assign_to_id)
            query.assign_to = assign_to
        query.save()
        return ""
    except ObjectDoesNotExist as e:
        message = "Task with this id is not found"
        return message


def UpdateTaskStatus(decision, change_details, task_id):
    try:
        query = Task.objects.get(id=task_id)
        query.status = decision
        if change_details:
            query.change_details = change_details
        query.save()
        return None
    except ObjectDoesNotExist as e:
        message = "Task with this id is not found"
        return message


def UpdateAssignTaskStatus(decision, task_id):
    try:
        query = Task.objects.get(id=task_id)
        query.status = decision
        query.save()
        return None
    except ObjectDoesNotExist as e:
        message = "Task with this id is not found"
        return message


def user_post_save(*args, **kwargs):
    user = User.objects.get(username=kwargs.get("instance"))

    if not Team.objects.filter(creator=kwargs.get("instance")):
        Team.create_user_team(user.username, user)


post_save.connect(user_post_save, sender=User)
