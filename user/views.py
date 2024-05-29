from django.db.models import Q, Count
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

from auths.helper import UserLoginRequiredMixin as LoginRequiredMixin
from auths.models import User
from user.helper import TaskDelete, UpdateTask, UpdateTaskStatus, UpdateAssignTaskStatus
from user.models import Task, Team


# Create your views here.

class Dashboard(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        query = Task.objects.filter(Q(creator=request.user) | Q(assign_to=request.user))
        team_members = Team.objects.filter(creator=request.user).aggregate(total_members=Count('members'))

        mytask = query.filter(creator=request.user)
        assign_tasks = query.filter(assign_to=request.user)

        total_assign_tasks = assign_tasks.count()
        pending_assign_task = assign_tasks.filter(status='pending').count()
        process_assign_task = assign_tasks.filter(status='process').count()
        review_assign_task = assign_tasks.filter(status='review').count()
        complete_assign_task = assign_tasks.filter(status='complete').count()

        total_mytask = mytask.count()
        pending_mytask = mytask.filter(status='pending').count()
        process_mytask = mytask.filter(status='process').count()
        review_mytask = mytask.filter(status='review').count()
        complete_mytask = mytask.filter(status='complete').count()

        context = {
            "mytask": mytask,
            "assign_tasks": assign_tasks,
            "total_members": team_members['total_members'],

            "total_mytask": total_mytask,
            "pending_mytask": pending_mytask,
            "process_mytask": process_mytask,
            "review_mytask": review_mytask,
            "complete_mytask": complete_mytask,

            "total_assign_tasks": total_assign_tasks,
            "pending_assign_task": pending_assign_task,
            "process_assign_task": process_assign_task,
            "review_assign_task": review_assign_task,
            "complete_assign_task": complete_assign_task,

        }
        return render(request, 'dashboard.html', context)


class AddTask(LoginRequiredMixin, View):

    @staticmethod
    def get(request):
        assign_user = User.objects.filter(team_members__creator=request.user).distinct()
        context = {"assign_user": assign_user}
        return render(request, "add_new_task.html", context)

    @staticmethod
    def post(request):
        data = request.POST
        title = data.get('task_title', None)
        deadline = data.get('deadline', None)
        assign = data.get('assign_to', None)
        task_details = data.get('task_details', None)
        message = Task.create_task(title, request.user, assign, deadline, task_details)
        if message:
            messages.error(request, message)
        else:
            messages.success(request, "New Task is Added Successfully")
        return redirect("/all_mytask/")


class MyTask(LoginRequiredMixin, View):

    @staticmethod
    def get(request):
        filter_status = request.GET.get("filter_status", None)
        mytask = Task.objects.filter(creator=request.user).exclude(status="complete")
        if filter_status:
            if filter_status != 'all':
                mytask = mytask.filter(status=str(filter_status))
        context = {"mytask": mytask}
        return render(request, "view_all_mytask.html", context)

    @staticmethod
    def post(request):
        data = request.POST
        action = data.get('action', None)
        task_id = data.get('task_id', None)

        if action == 'delete':
            message = TaskDelete(task_id)
            if message:
                messages.error(request, message)
            else:
                messages.success(request, "Task is Deleted Successfully")
        elif action == "update_btn":
            assign_user = User.objects.filter(team_members__creator=request.user).distinct()
            update_task = Task.objects.get(id=task_id)
            context = {"update_task": update_task, "assign_user": assign_user}
            return render(request, "update_task.html", context)
        elif action == 'update_task':
            data = request.POST
            task_title = data.get('task_title', None)
            assign_to = data.get('assign_to', None)
            deadline = data.get('deadline', None)
            task_details = data.get('task_details', None)

            message = UpdateTask(task_title, assign_to, deadline, task_details, task_id)
            if message:
                messages.error(request, message)
            else:
                messages.success(request, "Task is Updated Successfully")
        elif action == 'status':
            decision = data.get('decision', None)
            change_details = data.get('change_details', None)

            message = UpdateTaskStatus(decision, change_details, task_id)
            if message:
                messages.error(request, message)
            else:
                if change_details:
                    messages.success(request, 'Task change request is Submitted')
                else:
                    messages.success(request, 'Task status is completed successfully')

        return redirect('/all_mytask/')


class AssignTask(LoginRequiredMixin, View):

    @staticmethod
    def get(request):
        filter_status = request.GET.get("filter_status", None)
        assign_tasks = Task.objects.filter(assign_to=request.user).exclude(status="complete")
        if filter_status:
            if filter_status != 'all':
                assign_tasks = assign_tasks.filter(status=str(filter_status))
        context = {"assign_tasks": assign_tasks}
        return render(request, "view_all_assign_task.html", context)

    @staticmethod
    def post(request):
        data = request.POST
        action = data.get('action', None)
        task_id = data.get('task_id', None)
        decision = data.get('decision', None)

        if action == 'status':
            message = UpdateAssignTaskStatus(decision, task_id)
            if message:
                messages.error(request, message)
            else:
                if decision == 'review':
                    messages.success(request, 'Your Task is Under Review Now')
                else:
                    messages.success(request, 'Task status is start successfully')

        return redirect('/all_task/')


class MyCompleteTask(LoginRequiredMixin, View):

    @staticmethod
    def get(request):
        mytask = Task.objects.filter(creator=request.user, status='complete')
        context = {"mytask": mytask}
        return render(request, "complete_mytask.html", context)


class AssignCompleteTask(LoginRequiredMixin, View):

    @staticmethod
    def get(request):
        assign_tasks = Task.objects.filter(assign_to=request.user, status='complete')
        context = {"assign_tasks": assign_tasks}
        return render(request, "complete_assign_task.html", context)


class ViewMembers(LoginRequiredMixin, View):

    @staticmethod
    def get(request):
        query = User.objects.all().exclude(id=request.user.id)
        team_members = query.filter(team_members__creator=request.user).distinct()
        remaining_users = query.exclude(id__in=team_members.values_list('id', flat=True))
        context = {"team_members": team_members, "remaining_users": remaining_users}
        return render(request, "view_all_team_members.html", context)

    @staticmethod
    def post(request):
        data = request.POST
        member_id = data.get('member', None)
        try:
            user_team = Team.objects.get(creator=request.user)
            user_team.members.add(User.objects.get(id=member_id))
            user_team.save()
            messages.success(request, "New Member is added Successfully")
        except Exception as e:
            messages.success(request, "Internal Server Error")
        return redirect("/all_member/")
