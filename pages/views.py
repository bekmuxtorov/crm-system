from django.shortcuts import render
from django.views.generic import UpdateView, DeleteView, CreateView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.forms import CustomUserCreationForm
from accounts.models import CustomUser
from pages.const import Const
from . import models
import datetime as dt

# Create your views here.
class HomePageView(LoginRequiredMixin,TemplateView ):
    template_name = 'dashboard.html'


def StudentsPageView(request):
    context = {}
    students = models.Students.objects.all().order_by('-acceptance_date')
    context['students'] = students
    context['numbers'] = 1
    return render(request, 'pages/students.html', context)

def create_username(name: str, birthday: int) -> str:
    return f"st_{name.split(' ')[0].lower()[:4]}{birthday}"

def AddStudentsView(request):
    groups = models.Groups.objects.all()
    regions = dict(Const.regions)
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        acceptance_date = request.POST.get('acceptance_date')
        group_id = request.POST.get('group')
        group = models.Groups.objects.get(pk=group_id)
        birthday = request.POST.get('birthday')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        shartnoma_raqam = request.POST.get('shartnoma_raqam')
        PINFL_number = request.POST.get('PINFL_number')
        region_id = request.POST.get('region')
        region = list(dict(Const.regions).values())[int(region_id)-1]
        district = request.POST.get('district')
        username = create_username(first_name, birthday)
        models.Students(
            first_name = first_name,
            acceptance_date = acceptance_date,
            acceptance_group = group,
            birthday = birthday,
            phone_number = phone_number,
            email = email,
            shartnoma_raqami = shartnoma_raqam,
            PINFL_number = PINFL_number,
            region = region,
            district = district,
            username = username,
            parol = phone_number
        ).save()

        
        CustomUser.objects.create_user(username=username, password=phone_number, phone_number=phone_number)



    context = {
                'groups': groups,
                'regions':regions
            }
    return render(request, 'pages/add_students.html', context)

class UpdateStudentsView(UpdateView):
    model = models.Students
    fields = ['first_name', 'phone_number', 'email', 'shartnoma_raqami', 'PINFL_number', 'birthday', 'acceptance_date', 'acceptance_group', 'is_comleted']
    template_name = 'pages/update_students.html'

class DeleteStudentsView(DeleteView):
    model = models.Students
    template_name = 'pages/delete_students.html'
    success_url = reverse_lazy('students')

def ComplateStudentsView(request):
    objects = models.Students.objects.filter(is_comleted=True)
    context = {'students': objects}
    return render(request, 'pages/complate.html', context)

def SingleStudentsView(request, pk):
    object = models.Students.objects.get(pk=pk) 
    context = {'object': object}
    return render(request, 'pages/single_person.html', context)

# Groups section views
def GroupsPageView(request):
    objects = models.Groups.objects.all().order_by('-acceptance_date')
    student_count = models.Students.objects.filter()
    context = {'groups':objects}
    return render(request, 'pages/groups.html', context)

def GroupsAddPageView(request):
    status = False
    if request.method == "POST":
        name = request.POST.get('name')
        vaqt = request.POST.get('vaqt')
        days_id = request.POST.get('days')
        days = dict(Const.days)[days_id]
        duration = request.POST.get('duration')
        price = request.POST.get('price')
        teacher_id = request.POST.get('teacher')
        teacher = models.Employess.objects.get(pk=teacher_id)
        acceptance_date = request.POST.get('acceptance_date')
        models.Groups(name=name, vaqt=vaqt, acceptance_date=acceptance_date,duration =duration, days=days, price=price, teacher=teacher).save()
        status = True

    days = dict(Const.days)
    teachers = models.Employess.objects.all()
    context = {'teachers': teachers,
                'status': status,
                'days': days,
              }
    
    return render(request, 'pages/groups_add.html', context)

def GroupsCompletedView(request):
    objects = models.Groups.objects.filter(is_close=True)
    context = {'students': objects}
    return render(request, 'pages/groups_completed.html', context)

class GroupsDeleteView(DeleteView):
    model = models.Groups
    template_name = 'pages/groups_delete.html'
    success_url = reverse_lazy('groups')

class GroupsUpdateView(UpdateView):
    model = models.Groups
    fields = ['name', 'days', 'vaqt', 'price', 'acceptance_date', 'teacher', 'is_close', ]
    template_name = 'pages/groups_update.html'

def GroupsStudentsView(request, pk):
    group = models.Groups.objects.get(pk=pk)
    students = models.Students.objects.filter(acceptance_group=group)
    context = {
                'students': students,
                'group': group
              }
    return render(request, 'pages/groups_students.html', context)

# Teacher section
def TeacherListView(request):
    if request.method == 'POST':
        first_lastname = request.POST.get('first_lastname')
        science = request.POST.get('science')
        acceptance_date = request.POST.get('acceptance_date')
        phone_number = request.POST.get('phone_number')
        pasport = request.POST.get('pasport')
        models.Employess.objects.create(first_lastname = first_lastname,
                                        science = science, 
                                        acceptance_date = acceptance_date,
                                        pasport = pasport,
                                        phone_number = phone_number    
                                        )
    teachers = models.Employess.objects.all().order_by('-acceptance_date')
    context = {'teachers': teachers}
    return render(request, 'pages/teachers.html', context)

class TeacherDeleteView(DeleteView):
    model = models.Employess
    template_name = 'pages/teachers_delete.html'
    success_url = reverse_lazy('teachers')

class TeacherUpdateView(UpdateView):
    model = models.Employess
    fields = ['first_lastname', 'acceptance_date', 'pasport', 'phone_number', 'science']
    template_name = 'pages/teachers_update.html'

# Payments

def get_date(date):
    return date.strftime("%d/%m/%Y")

def PaymentDays(n,acceptance_date: dt, days_id: int=1, ) -> list[str]:
    acceptance_date_month = acceptance_date.month
    if acceptance_date_month + 1 <= 12: 
        next_date_month = acceptance_date_month + 1
        date_year = acceptance_date.year

    else:  
        next_date_month = (acceptance_date_month + 1) % 12
        date_year = acceptance_date.year + 1
    count = {'1': f'{get_date(acceptance_date)} >> {get_date(dt.date(date_year, next_date_month, 1))}'}

    for i in range(n):
        if next_date_month + 1 <= 12: next_date_month = next_date_month + 1 
        else: 
            next_date_month = (next_date_month + 1) % 12 
            date_year += 1

        count[i+1] = f'{get_date(dt.date(date_year, next_date_month, 1))}'
        

    return count 

def PaymentsPageView(request):
    groups = models.Groups.objects.all()
    
    context = {'groups': groups}
    return render(request, 'pages/payments.html', context)

def PaymentsGroups(request, pk):
    choose_group = models.Groups.objects.get(pk=pk)
    n = choose_group.duration
    students = models.Students.objects.all().filter(acceptance_group=choose_group)
    count = PaymentDays(n,choose_group.acceptance_date) 
    context = {
                'choose_group': choose_group,
                'count':count,
                'students':students
              }

    print(count)
    return render(request, 'pages/payments_groups.html', context)

def OthersPaymentsView(request):
    return render(request, 'pages/payments_others.html')

def AddPaymentsView(request):
    students = models.Students.objects.all().order_by('-acceptance_date')
    context = {'students': students}
    return render(request, 'pages/payments_add.html', context)

# Accounts
def AccountsSingleView(request):
    return render(request, 'pages/single_person.html')