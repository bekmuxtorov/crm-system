from django.shortcuts import render
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy
from accounts.forms import CustomUserCreationForm
from accounts.models import CustomUser
from pages.const import Const
from . import models

# Create your views here.
def HomePageView(request):
    return render(request, 'dashboard.html')

def StudentsPageView(request):
    context = {}
    students = models.Students.objects.all().order_by('-acceptance_date')
    context['students'] = students
    context['numbers'] = 1
    return render(request, 'pages/students.html', context)

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
            district = district
        ).save()
        CustomUser(username=first_name[:4], password=phone_number, phone_number= phone_number).save()


    context = {
                'groups': groups,
                'regions':regions
            }
    return render(request, 'pages/add_students.html', context)

class UpdateStudentsView(UpdateView):
    model = models.Students
    fields = ['first_name', 'phone_number', 'email', 'shartnoma_raqami', 'PINFL_number', 'birthday', 'acceptance_date', 'acceptance_group', 'region', 'district', 'is_comleted']
    template_name = 'pages/update_students.html'

class DeleteStudentsView(DeleteView):
    model = models.Students
    template_name = 'pages/delete_students.html'
    success_url = reverse_lazy('students')

def ComplateStudentsView(request):
    objects = models.Students.objects.filter(is_comleted=True)
    context = {'students': objects}
    return render(request, 'pages/complate.html', context)

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
        teacher_id = request.POST.get('teacher')
        teacher = models.Employess.objects.get(pk=teacher_id)
        acceptance_date = request.POST.get('acceptance_date')
        models.Groups(name=name, vaqt=vaqt, acceptance_date=acceptance_date, teacher=teacher).save()
        status = True

    teachers = models.Employess.objects.all()
    context = {'teachers': teachers,
                'status': status
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
    fields = ['name', 'vaqt', 'acceptance_date', 'teacher', 'is_close']
    template_name = 'pages/groups_update.html'

def GroupsStudentsView(request, pk):
    group = models.Groups.objects.get(pk=pk)
    students = models.Students.objects.filter(acceptance_group=group)
    context = {
                'students': students,
                'group': group
              }
    return render(request, 'pages/groups_students.html', context)
