from sched import scheduler
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound

from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from django.urls import reverse

import datetime
import time

from django.db import models
from django.db.models import Q

import csv
import xlwt
from io import BytesIO

# Подключение моделей
from .models import Teachers, Training, Groups, Members, Schedule, Payment, Reviews, Claim, News
# Подключение форм
from .forms import TeachersForm, TrainingForm, GroupsForm, MembersForm, ScheduleForm, PaymentForm, ReviewsForm, ClaimForm, ClaimFormEdit, NewsForm, SignUpForm

# Подключение моделей
from django.contrib.auth.models import User, Group, AnonymousUser
from django.contrib.auth import login as auth_login

# Create your views here.
# Групповые ограничения
def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups, login_url='403')

# Стартовая страница 
def index(request):
    reviews = Reviews.objects.exclude(rating=None).order_by('?')[0:4]
    teachers = Teachers.objects.all().order_by('?')[0:6]   
    return render(request, "index.html", {"reviews": reviews, "teachers": teachers})    

# Контакты
def contact(request):
    return render(request, "contact.html")

# Страница FAQ
def faq(request):
    return render(request, "faq.html")

# Кабинет
@login_required
def cabinet(request):
    members = Members.objects.filter(user_id=request.user.id).order_by('groups', 'user')

    schedule = Schedule.objects.raw("""
SELECT schedule.id, schedule.dates, groups.title AS groups_title, training.title AS training_title, auth_user.username
FROM auth_user
INNER JOIN members ON auth_user.id = members.user_id
INNER JOIN groups ON members.groups_id = groups.id
INNER JOIN training ON groups.training_id = training.id
INNER JOIN schedule ON schedule.groups_id = members.groups_id
WHERE auth_user.username = %s
ORDER BY schedule.dates DESC, groups.title, training.title
""", params=[request.user.username])

    #for s in schedule:
    #    print(s.dates, s.groups_title, s.training_title)

    user_info = request.user.first_name + " " +request.user.last_name + " (" + request.user.username + ")"
    
    payment = Payment.objects.filter(user_id=request.user.id).order_by('-datep')
    return render(request, "cabinet.html", {"members": members, "schedule": schedule, "payment": payment, "user_info": user_info})

# Список для просмотра
def teachers_list(request):
    teachers = Teachers.objects.all().order_by('surname', 'name', 'patronymic')
    return render(request, "teachers/list.html", {"teachers": teachers})

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def teachers_index(request):
    teachers = Teachers.objects.all().order_by('surname', 'name', 'patronymic')
    return render(request, "teachers/index.html", {"teachers": teachers})

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def teachers_create(request):
    try:
        if request.method == "POST":
            teachers = Teachers()        
            teachers.surname = request.POST.get("surname")
            teachers.name = request.POST.get("name")
            teachers.patronymic = request.POST.get("patronymic")
            teachers.details = request.POST.get("details")
            if 'photo' in request.FILES:                
                teachers.photo = request.FILES['photo']
            teachersform = TeachersForm(request.POST)
            if teachersform.is_valid():
                teachers.save()
                return HttpResponseRedirect(reverse('teachers_index'))
            else:
                return render(request, "teachers/create.html", {"form": teachersform})
        else:        
            teachersform = TeachersForm()
        return render(request, "teachers/create.html", {"form": teachersform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
@group_required("Managers")
def teachers_edit(request, id):
    try:
        teachers = Teachers.objects.get(id=id) 
        if request.method == "POST":
            teachers.surname = request.POST.get("surname")
            teachers.name = request.POST.get("name")
            teachers.patronymic = request.POST.get("patronymic")
            teachers.details = request.POST.get("details")
            if "photo" in request.FILES:                
                teachers.photo = request.FILES["photo"]
            teachersform = TeachersForm(request.POST)
            if teachersform.is_valid():
                teachers.save()
                return HttpResponseRedirect(reverse('teachers_index'))
            else:
                return render(request, "teachers/edit.html", {"form": teachersform})                
        else:
            # Загрузка начальных данных
            teachersform = TeachersForm(initial={'surname': teachers.surname, 'name': teachers.name, 'patronymic': teachers.patronymic, 'details': teachers.details, 'photo': teachers.photo  })
            return render(request, "teachers/edit.html", {"form": teachersform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def teachers_delete(request, id):
    try:
        teachers = Teachers.objects.get(id=id)
        teachers.delete()
        return HttpResponseRedirect(reverse('teachers_index'))
    except Teachers.DoesNotExist:
        return HttpResponseNotFound("<h2>Teachers not found</h2>")

# Просмотр страницы read.html для просмотра объекта.
@login_required
def teachers_read(request, id):
    try:
        teachers = Teachers.objects.get(id=id) 
        return render(request, "teachers/read.html", {"teachers": teachers})
    except Teachers.DoesNotExist:
        return HttpResponseNotFound("<h2>Teachers not found</h2>")

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def training_index(request):
    training = Training.objects.all().order_by('title')
    return render(request, "training/index.html", {"training": training})

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def training_create(request):
    if request.method == "POST":
        training = Training()        
        training.title = request.POST.get("title")
        training.details = request.POST.get("details")
        trainingform = TrainingForm(request.POST)
        if trainingform.is_valid():
            training.save()
            return HttpResponseRedirect(reverse('training_index'))
        else:
            return render(request, "training/create.html", {"form": trainingform})                
    else:        
        trainingform = TrainingForm()
        return render(request, "training/create.html", {"form": trainingform})

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
@group_required("Managers")
def training_edit(request, id):
    try:
        training = Training.objects.get(id=id) 
        if request.method == "POST":
            training.title = request.POST.get("title")
            training.details = request.POST.get("details")
            trainingform = TrainingForm(request.POST)
            if trainingform.is_valid():
                training.save()
                return HttpResponseRedirect(reverse('training_index'))
            else:
                return render(request, "training/edit.html", {"form": trainingform})  
        else:
            # Загрузка начальных данных
            trainingform = TrainingForm(initial={'title': training.title, 'details': training.details })
            return render(request, "training/edit.html", {"form": trainingform})
    except Training.DoesNotExist:
        return HttpResponseNotFound("<h2>Training not found</h2>")

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def training_delete(request, id):
    try:
        training = Training.objects.get(id=id)
        training.delete()
        return HttpResponseRedirect(reverse('training_index'))
    except Training.DoesNotExist:
        return HttpResponseNotFound("<h2>Training not found</h2>")

# Просмотр страницы read.html для просмотра объекта.
@login_required
def training_read(request, id):
    try:
        training = Training.objects.get(id=id) 
        return render(request, "training/read.html", {"training": training})
    except Training.DoesNotExist:
        return HttpResponseNotFound("<h2>Training not found</h2>")

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def groups_index(request):
    groups = Groups.objects.all().order_by('title')
    return render(request, "groups/index.html", {"groups": groups})

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def groups_create(request):
    if request.method == "POST":
        groups = Groups()        
        groups.training = Training.objects.filter(id=request.POST.get("training")).first()
        groups.title = request.POST.get("title")
        groups.details = request.POST.get("details")
        groups.teachers = Teachers.objects.filter(id=request.POST.get("teachers")).first()
        groupsform = GroupsForm(request.POST)
        if groupsform.is_valid():
            groups.save()
            return HttpResponseRedirect(reverse('groups_index'))
        else:
            return render(request, "groups/create.html", {"form": groupsform})                
    else:        
        groupsform = GroupsForm()
        return render(request, "groups/create.html", {"form": groupsform})

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
@group_required("Managers")
def groups_edit(request, id):
    try:
        groups = Groups.objects.get(id=id) 
        if request.method == "POST":
            groups.training = Training.objects.filter(id=request.POST.get("training")).first()
            groups.title = request.POST.get("title")
            groups.details = request.POST.get("details")
            groups.teachers = Teachers.objects.filter(id=request.POST.get("teachers")).first()
            groupsform = GroupsForm(request.POST)
            if groupsform.is_valid():
                groups.save()
                return HttpResponseRedirect(reverse('groups_index'))
            else:
                return render(request, "groups/edit.html", {"form": groupsform})  
        else:
            # Загрузка начальных данных
            groupsform = GroupsForm(initial={'training': groups.training, 'title': groups.title, 'details': groups.details, 'teachers': groups.teachers })
            return render(request, "groups/edit.html", {"form": groupsform})
    except Groups.DoesNotExist:
        return HttpResponseNotFound("<h2>Groups not found</h2>")

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def groups_delete(request, id):
    try:
        groups = Groups.objects.get(id=id)
        groups.delete()
        return HttpResponseRedirect(reverse('groups_index'))
    except Groups.DoesNotExist:
        return HttpResponseNotFound("<h2>Groups not found</h2>")

# Просмотр страницы read.html для просмотра объекта.
@login_required
def groups_read(request, id):
    try:
        groups = Groups.objects.get(id=id) 
        members = Members.objects.filter(groups_id=id).order_by('groups', 'user')
        return render(request, "groups/read.html", {"groups": groups, "members": members})
    except Groups.DoesNotExist:
        return HttpResponseNotFound("<h2>Groups not found</h2>")

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def members_index(request):
    members = Members.objects.all().order_by('groups', 'user')
    return render(request, "members/index.html", {"members": members})

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def members_create(request):
    if request.method == "POST":
        members = Members()        
        members.groups = Groups.objects.filter(id=request.POST.get("groups")).first()
        members.user = User.objects.filter(id=request.POST.get("user")).first()
        membersform = MembersForm(request.POST)
        if membersform.is_valid():
            members.save()
            return HttpResponseRedirect(reverse('members_index'))
        else:
            return render(request, "members/create.html", {"form": membersform})                
    else:        
        membersform = MembersForm()
        return render(request, "members/create.html", {"form": membersform})

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
@group_required("Managers")
def members_edit(request, id):
    try:
        members = Members.objects.get(id=id) 
        if request.method == "POST":
            members.groups = Groups.objects.filter(id=request.POST.get("groups")).first()
            members.user = User.objects.filter(id=request.POST.get("user")).first()
            membersform = MembersForm(request.POST)
            if membersform.is_valid():
                members.save()
                return HttpResponseRedirect(reverse('members_index'))
            else:
                return render(request, "members/edit.html", {"form": membersform})  
        else:
            # Загрузка начальных данных
            membersform = MembersForm(initial={'groups': members.groups, 'user': members.user })
            return render(request, "members/edit.html", {"form": membersform})
    except Members.DoesNotExist:
        return HttpResponseNotFound("<h2>Members not found</h2>")

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def members_delete(request, id):
    try:
        members = Members.objects.get(id=id)
        members.delete()
        return HttpResponseRedirect(reverse('members_index'))
    except Members.DoesNotExist:
        return HttpResponseNotFound("<h2>Members not found</h2>")

# Просмотр страницы read.html для просмотра объекта.
@login_required
def members_read(request, id):
    try:
        members = Members.objects.get(id=id) 
        return render(request, "members/read.html", {"members": members})
    except Members.DoesNotExist:
        return HttpResponseNotFound("<h2>Members not found</h2>")

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def schedule_index(request):
    schedule = Schedule.objects.all().order_by('dates', 'groups')
    return render(request, "schedule/index.html", {"schedule": schedule})

# Список для просмотра
@login_required
def schedule_list(request):
    try:
        schedule = Schedule.objects.all().order_by('-dates', 'groups')
        return render(request, "schedule/list.html", {"schedule": schedule})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def schedule_create(request):
    if request.method == "POST":
        schedule = Schedule()       
        scheduleform = ScheduleForm(request.POST)        
        dt = request.POST.get("dates")
        try:
            #print(dt)
            valid_date = time.strptime(dt, '%Y-%m-%d %H:%M:%S')          
        except ValueError:
            return render(request, "schedule/create.html", {"form": scheduleform}) 
        schedule.dates = datetime.datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
        #schedule.dates = datetime.datetime.strptime(request.POST.get("dates"), '%Y-%m-%d %H:%M:%S')
        schedule.groups = Groups.objects.filter(id=request.POST.get("groups")).first()
        if scheduleform.is_valid():
            schedule.save()
            return HttpResponseRedirect(reverse('schedule_index'))
        else:
            return render(request, "schedule/create.html", {"form": scheduleform})                
    else:        
        scheduleform = ScheduleForm(initial={'dates': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), })
        return render(request, "schedule/create.html", {"form": scheduleform})
    
# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
@group_required("Managers")
def schedule_edit(request, id):
    try:
        schedule = Schedule.objects.get(id=id) 
        if request.method == "POST":
            scheduleform = ScheduleForm(request.POST)            
            dt = request.POST.get("dates")
            try:
                print(dt)
                valid_date = time.strptime(dt, '%Y-%m-%d %H:%M:%S')          
            except ValueError:
                return render(request, "schedule/edit.html", {"form": scheduleform}) 
            schedule.dates = datetime.datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
            #schedule.dates = datetime.datetime.strptime(request.POST.get("dates"), '%Y-%m-%d %H:%M:%S')      
            schedule.groups = Groups.objects.filter(id=request.POST.get("groups")).first()
            if scheduleform.is_valid():
                schedule.save()
                return HttpResponseRedirect(reverse('schedule_index'))
            else:
                return render(request, "schedule/edit.html", {"form": scheduleform})  
        else:
            # Загрузка начальных данных
            scheduleform = ScheduleForm(initial={'dates': schedule.dates.strftime('%Y-%m-%d %H:%M:%S'), 'groups': schedule.groups })
            return render(request, "schedule/edit.html", {"form": scheduleform})
    except Schedule.DoesNotExist:
        return HttpResponseNotFound("<h2>Schedule not found</h2>")

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def schedule_delete(request, id):
    try:
        schedule = Schedule.objects.get(id=id)
        schedule.delete()
        return HttpResponseRedirect(reverse('schedule_index'))
    except Schedule.DoesNotExist:
        return HttpResponseNotFound("<h2>Schedule not found</h2>")

# Просмотр страницы read.html для просмотра объекта.
@login_required
def schedule_read(request, id):
    try:
        schedule = Schedule.objects.get(id=id) 
        return render(request, "schedule/read.html", {"schedule": schedule})
    except Schedule.DoesNotExist:
        return HttpResponseNotFound("<h2>Schedule not found</h2>")

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def payment_index(request):
    payment = Payment.objects.all().order_by('datep')
#    report = Payment.objects.raw("""
#SELECT 1 as id, strftime('%Y', payment.datep) as year, strftime('%m', payment.datep) as month, auth_user.last_name, auth_user.first_name, auth_user.username, SUM(payment.amount) AS amount,
#(SELECT SUM(p.amount) FROM payment p WHERE  p.user_id = payment.user_id) as total
#FROM payment LEFT JOIN auth_user ON payment.user_id = auth_user.id
#GROUP BY strftime('%Y', payment.datep), strftime('%m', payment.datep), auth_user.last_name, auth_user.first_name, auth_user.username
#""")
    report = Payment.objects.raw("""
SELECT 1 as id,  date_part('year', payment.datep) as year, date_part('month', payment.datep) as month, payment.user_id, auth_user.last_name, auth_user.first_name, auth_user.username, SUM(payment.amount) AS amount,
(SELECT SUM(p.amount) FROM payment p WHERE  p.user_id = payment.user_id) as total
FROM payment LEFT JOIN auth_user ON payment.user_id = auth_user.id
GROUP BY date_part('year', payment.datep), date_part('month', payment.datep), payment.user_id, auth_user.last_name, auth_user.first_name, auth_user.username
""")
    return render(request, "payment/index.html", {"payment": payment, "report": report})

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def payment_create(request):
    if request.method == "POST":
        payment = Payment()        
        paymentform = PaymentForm(request.POST)
        dt = request.POST.get("datep")
        try:
            #print(dt)
            valid_date = time.strptime(dt, '%Y-%m-%d %H:%M:%S')          
        except ValueError:
            return render(request, "payment/create.html", {"form": paymentform}) 
        payment.datep = datetime.datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')        
        #payment.datep = datetime.datetime.strptime(request.POST.get("datep"), '%Y-%m-%d %H:%M')        
        payment.amount = request.POST.get("amount")
        payment.user = User.objects.filter(id=request.POST.get("user")).first()
        if paymentform.is_valid():
            payment.save()
            return HttpResponseRedirect(reverse('payment_index'))
        else:
            return render(request, "payment/create.html", {"form": paymentform})                
    else:        
        paymentform = PaymentForm(initial={'datep': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), })
        return render(request, "payment/create.html", {"form": paymentform})
    
# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
@group_required("Managers")
def payment_edit(request, id):
    try:
        payment = Payment.objects.get(id=id) 
        if request.method == "POST":
            paymentform = PaymentForm(request.POST)
            dt = request.POST.get("datep")
            try:
                #print(dt)
                valid_date = time.strptime(dt, '%Y-%m-%d %H:%M:%S')          
            except ValueError:
                return render(request, "payment/edit.html", {"form": paymentform}) 
            payment.datep = datetime.datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')                
            #payment.datep = datetime.datetime.strptime(request.POST.get("datep"), '%Y-%m-%d %H:%M')
            payment.amount = request.POST.get("amount")
            payment.user = User.objects.filter(id=request.POST.get("user")).first()
            if paymentform.is_valid():
                payment.save()
                return HttpResponseRedirect(reverse('payment_index'))
            else:
                return render(request, "payment/edit.html", {"form": paymentform})  
        else:
            # Загрузка начальных данных
            paymentform = PaymentForm(initial={'datep': payment.datep.strftime('%Y-%m-%d %H:%M:%S'), 'amount': payment.amount, 'user': payment.user })
            return render(request, "payment/edit.html", {"form": paymentform})
    except Payment.DoesNotExist:
        return HttpResponseNotFound("<h2>Payment not found</h2>")

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def payment_delete(request, id):
    try:
        payment = Payment.objects.get(id=id)
        payment.delete()
        return HttpResponseRedirect(reverse('payment_index'))
    except Payment.DoesNotExist:
        return HttpResponseNotFound("<h2>Payment not found</h2>")

# Просмотр страницы read.html для просмотра объекта.
@login_required
def payment_read(request, id):
    try:
        payment = Payment.objects.get(id=id) 
        return render(request, "payment/read.html", {"payment": payment})
    except Payment.DoesNotExist:
        return HttpResponseNotFound("<h2>Payment not found</h2>")

# Список для просмотра
def reviews_list(request):
    reviews = Reviews.objects.all().order_by('-dater')
    return render(request, "reviews/list.html", {"reviews": reviews})

# Список для просмотра с кнопкой удалить
@login_required
@group_required("Managers")
def reviews_index(request):
    reviews = Reviews.objects.all().order_by('-dater')
    return render(request, "reviews/index.html", {"reviews": reviews})

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
def reviews_create(request):
    if request.method == "POST":
        reviews = Reviews()        
        reviews.rating = request.POST.get("rating")
        reviews.details = request.POST.get("details")
        reviews.user = request.user
        reviewsform = ReviewsForm(request.POST)
        if reviewsform.is_valid():
            reviews.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "reviews/create.html", {"form": reviewsform})     
    else:        
        reviewsform = ReviewsForm(initial={'rating': 5, })
        return render(request, "reviews/create.html", {"form": reviewsform})

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def reviews_delete(request, id):
    try:
        reviews = Reviews.objects.get(id=id)
        reviews.delete()
        return HttpResponseRedirect(reverse('reviews_index'))
    except Reviews.DoesNotExist:
        return HttpResponseNotFound("<h2>Reviews not found</h2>")

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def claim_index(request):
    claim = Claim.objects.all().order_by('-dater')
    return render(request, "claim/index.html", {"claim": claim})

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
def claim_create(request):
    if request.method == "POST":
        claim = Claim()        
        claim.user = request.user
        claim.training = Training.objects.filter(id=request.POST.get("training")).first()
        claim.details = request.POST.get("details")
        claim.result = ""
        claimform = ClaimForm(request.POST)
        if claimform.is_valid():
            claim.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "claim/create.html", {"form": claimform})     
    else:        
        claimform = ClaimForm()
        return render(request, "claim/create.html", {"form": claimform})

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
@group_required("Managers")
def claim_edit(request, id):
    try:
        claim = Claim.objects.get(id=id) 
        if request.method == "POST":
            claim.result = request.POST.get("result")
            claimform = ClaimFormEdit(request.POST)
            if claimform.is_valid():                   
                claim.save()
                return HttpResponseRedirect(reverse('claim_index'))
            else:
                return render(request, "claim/edit.html", {"form": claimform})  
        else:
            # Загрузка начальных данных
            claimform = ClaimFormEdit(initial={ 'result': claim.result })
            return render(request, "claim/edit.html", {"form": claimform, 'dater': claim.dater, 'user': claim.user, 'training': claim.training, 'details': claim.details})
    except Claim.DoesNotExist:
        return HttpResponseNotFound("<h2>Claim not found</h2>")

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def claim_delete(request, id):
    try:
        claim = Claim.objects.get(id=id)
        claim.delete()
        return HttpResponseRedirect(reverse('claim_index'))
    except Claim.DoesNotExist:
        return HttpResponseNotFound("<h2>Claim not found</h2>")

# Просмотр страницы read.html для просмотра объекта.
@login_required
def claim_read(request, id):
    try:
        claim = Claim.objects.get(id=id) 
        return render(request, "claim/read.html", {"claim": claim})
    except Claim.DoesNotExist:
        return HttpResponseNotFound("<h2>Claim not found</h2>")

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def news_index(request):
    #news = News.objects.all().order_by('surname', 'name', 'patronymic')
    #return render(request, "news/index.html", {"news": news})
    news = News.objects.all().order_by('-daten')
    return render(request, "news/index.html", {"news": news})

# Список для просмотра
def news_list(request):
    news = News.objects.all().order_by('-daten')
    return render(request, "news/list.html", {"news": news})

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def news_create(request):
    try:
        if request.method == "POST":
            news = News()        
            news.daten = request.POST.get("daten")
            news.title = request.POST.get("title")
            news.details = request.POST.get("details")
            if 'photo' in request.FILES:                
                news.photo = request.FILES['photo']   
            newsform = NewsForm(request.POST)
            if newsform.is_valid():
                news.save()
                return HttpResponseRedirect(reverse('news_index'))
            else:
                return render(request, "news/create.html", {"form": newsform})
        else:        
            newsform = NewsForm(initial={'daten': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), })
            return render(request, "news/create.html", {"form": newsform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
@group_required("Managers")
def news_edit(request, id):
    try:
        news = News.objects.get(id=id) 
        if request.method == "POST":
            news.daten = request.POST.get("daten")
            news.title = request.POST.get("title")
            news.details = request.POST.get("details")
            if "photo" in request.FILES:                
                news.photo = request.FILES["photo"]
            newsform = NewsForm(request.POST)
            if newsform.is_valid():
                news.save()
                return HttpResponseRedirect(reverse('news_index'))
            else:
                return render(request, "news/edit.html", {"form": newsform})
        else:
            # Загрузка начальных данных
            newsform = NewsForm(initial={'daten': news.daten.strftime('%Y-%m-%d %H:%M:%S'), 'title': news.title, 'details': news.details, 'photo': news.photo })
            return render(request, "news/edit.html", {"form": newsform})
    except News.DoesNotExist:
        return HttpResponseNotFound("<h2>News not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)


# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def news_delete(request, id):
    try:
        news = News.objects.get(id=id)
        news.delete()
        return HttpResponseRedirect(reverse('news_index'))
    except News.DoesNotExist:
        return HttpResponseNotFound("<h2>News not found</h2>")

# Просмотр страницы read.html для просмотра объекта.
@login_required
def news_read(request, id):
    try:
        news = News.objects.get(id=id) 
        return render(request, "news/read.html", {"news": news})
    except News.DoesNotExist:
        return HttpResponseNotFound("<h2>News not found</h2>")

# Регистрационная форма 
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return HttpResponseRedirect(reverse('index'))
            #return render(request, 'registration/register_done.html', {'new_user': user})
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

# Экспорт в Excel
def export_excel(request): 
    # Create a HttpResponse object and set its content_type header value to Microsoft excel.
    response = HttpResponse(content_type='application/vnd.ms-excel') 
    # Set HTTP response Content-Disposition header value. Tell web server client the attached file name is students.xls.
    response['Content-Disposition'] = 'attachment;filename=report.xls' 
    # Create a new Workbook file.
    work_book = xlwt.Workbook(encoding = 'utf-8') 
    # Create a new worksheet in the above workbook.
    work_sheet = work_book.add_sheet(u'Catalog Info')
    # Maintain some worksheet styles，style_head_row, style_data_row, style_green, style_red
    # This style will be applied to worksheet head row.
    style_head_row = xlwt.easyxf("""    
        align:
          wrap off,
          vert center,
          horiz center;
        borders:
          left THIN,
          right THIN,
          top THIN,
          bottom THIN;
        font:
          name Arial,
          colour_index white,
          bold on,
          height 0xA0;
        pattern:
          pattern solid,
          fore-colour 0x19;
        """
    )
    # Define worksheet data row style. 
    style_data_row = xlwt.easyxf("""
        align:
          wrap on,
          vert center,
          horiz left;
        font:
          name Arial,
          bold off,
          height 0XA0;
        borders:
          left THIN,
          right THIN,
          top THIN,
          bottom THIN;
        """
    )
    # Set data row date string format.
    #style_data_row.num_format_str = 'dd/mm/yyyy'
    # Define a green color style.
    style_green = xlwt.easyxf(" pattern: fore-colour 0x11, pattern solid;")
    # Define a red color style.
    style_red = xlwt.easyxf(" pattern: fore-colour 0x0A, pattern solid;")
    # Generate worksheet head row data.
    work_sheet.write(0,0, str(_('year')), style_head_row) 
    work_sheet.write(0,1, str(_('month')), style_head_row) 
    work_sheet.write(0,2, str(_('user')), style_head_row) 
    work_sheet.write(0,3, str(_('amount')), style_head_row) 
    work_sheet.write(0,4, str(_('total')), style_head_row) 
    report = Payment.objects.raw("""
        SELECT 1 as id, strftime('%Y', payment.datep) as year, strftime('%m', payment.datep) as month, auth_user.last_name, auth_user.first_name, auth_user.username, SUM(payment.amount) AS amount,
        (SELECT SUM(p.amount) FROM payment p WHERE  p.user_id = payment.user_id) as total
        FROM payment LEFT JOIN auth_user ON payment.user_id = auth_user.id
        GROUP BY strftime('%Y', payment.datep), strftime('%m', payment.datep), auth_user.last_name, auth_user.first_name, auth_user.username
        """)
    # Generate worksheet data row data.
    row = 1 
    for r in report:
        work_sheet.write(row,0, r.year, style_data_row)
        work_sheet.write(row,1, r.month, style_data_row)
        work_sheet.write(row,2, r.last_name + ' ' + r.first_name, style_data_row)
        work_sheet.write(row,3, r.amount, style_data_row)
        work_sheet.write(row,4, r.total, style_data_row)
        row=row + 1 
    # Create a StringIO object.
    output = BytesIO()
    # Save the workbook data to the above StringIO object.
    work_book.save(output)
    # Reposition to the beginning of the StringIO object.
    output.seek(0)
    # Write the StringIO object's value to HTTP response to send the excel file to the web server client.
    response.write(output.getvalue()) 
    return response

# Изменение данных пользователя
@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email',)
    template_name = 'registration/my_account.html'
    success_url = reverse_lazy('index')
    #success_url = reverse_lazy('my_account')
    def get_object(self):
        return self.request.user

# Выход
from django.contrib.auth import logout
def logoutUser(request):
    logout(request)
    return render(request, "index.html")

