from django.shortcuts import render, redirect
from .models import Users, Jobs
from django.contrib import messages
import bcrypt
from datetime import date, datetime

# Create your views here.

def index(request):
    
    return render(request, 'index.html')

def register(request):
    errors = Users.objects.register_validator(request.POST)
    request.session['type'] = 1
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')

    pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode() 
    print(bcrypt.checkpw(request.POST['password'].encode(), pw_hash.encode()))

    Users.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'],
        password = pw_hash,
        birthday = request.POST['birthday']
    )

    request.session['userid'] = Users.objects.last().id
    return redirect('/dashboard')

def login(request):

    errors = Users.objects.login_validator(request.POST)
    request.session['type'] = 2
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')

    user = Users.objects.filter(email = request.POST['email'])
    if user:
        logged_user = user[0]

        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['userid'] = logged_user.id
            return redirect('/dashboard')

    
    return redirect('/')
    
def logout(request):
    request.session.clear()
    return redirect('/')

def dashboard(request):
    if len(request.session.keys()) == 0:
        return redirect('/')
    context = {
        'user' : Users.objects.get(id=  request.session['userid']),
        'jobs' : Jobs.objects.all()
    }
    

    return render(request,'dashboard.html', context)
    
def new_job(request):
    if len(request.session.keys()) == 0:
        return redirect('/')
    context = {
        'user' : Users.objects.get(id = request.session['userid'])
    }
    return render(request, 'new_job.html', context)

def new_job_process(request):
    errors = Jobs.objects.create_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/jobs/new')
    else:
        category = ''
        try :
            category += request.POST['pet_care'] + ','
        except:
            print('not work')
        try :
            category += request.POST['electrical'] + ','
        except:
            print('not work')
        try :
            category += request.POST['garden'] + ','
        except:
            print('not work')
        try :
            category += request.POST['other']
        except:
            print('not work')

        Jobs.objects.create(
            title = request.POST['title'],
            desc = request.POST['desc'],
            location = request.POST['location'],
            category = category,
            worked_on = True
            )
        user = Users.objects.get(id = request.session['userid'])
        job = Jobs.objects.last()
        user.job.add(job)
        return redirect('/dashboard')
    
def show_job(request, num):
    context = {
        'user' : Users.objects.get(id = request.session['userid']),
        'job' : Jobs.objects.get(id=num)
    }
    return render(request, 'show_job.html', context)

def edit_job(request, num):
    context = {
        'user' : Users.objects.get(id = request.session['userid']),
        'job' : Jobs.objects.get(id= num)
    }
    return render(request, 'edit_job.html', context)

def edit_job_process(request, num):
    errors = Jobs.objects.create_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/jobs/edit/' + num)
    else:
        job = Jobs.objects.get(id = num)
        job.title = request.POST['title']
        job.desc = request.POST['desc']
        job.location = request.POST['location']
        job.save()
        return redirect('/dashboard')

def remove(request, num):
    job = Jobs.objects.get(id=num)
    job.delete()
    return redirect('/dashboard')

def give_up(request, num):
    user = Users.objects.get(id = request.session['userid'])
    job = Jobs.objects.get(id=num)

    if (user.id != job.users.first().id):
        job.users.remove(user)

    job.worked_on = False
    job.save()
    return redirect('/dashboard')

def add(request, num):
    user = Users.objects.get(id = request.session['userid'])
    job = Jobs.objects.get(id = num )

    if (user.id != job.users.first().id):
        job.users.add(user)
    
    job.worked_on = True
    job.save()
    return redirect('/dashboard')