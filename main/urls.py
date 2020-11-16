from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('dashboard', views.dashboard),
    path('jobs/new', views.new_job),
    path('jobs/new/process', views.new_job_process),
    path('jobs/<num>', views.show_job),
    path('jobs/edit/<num>', views.edit_job),
    path('jobs/edit/process/<num>', views.edit_job_process),
    path('jobs/remove/<num>', views.remove),
    path('jobs/giveup/<num>', views.give_up),
    path('jobs/add/<num>', views.add)
]