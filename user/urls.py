from django.contrib.auth.views import LogoutView
from django.urls import path

from user import views

urlpatterns = [
    path("", views.Dashboard.as_view(), name="user_dashboard"),

    path('add_task/', views.AddTask.as_view(), name="add_task"),
    path('all_mytask/', views.MyTask.as_view(), name="all_mytask"),
    path('complete_mytask/', views.MyCompleteTask.as_view(), name="complete_mytask"),

    path('all_task/', views.AssignTask.as_view(), name="all_task"),
    path('complete_task/', views.AssignCompleteTask.as_view(), name='complete_task'),

    path('all_member/', views.ViewMembers.as_view(), name='all_member'),
]
