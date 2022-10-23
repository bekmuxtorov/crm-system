from django.contrib import admin
from . import models
# Register your models here.

class AdminStudents(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'acceptance_group', 'phone_number', 'acceptance_date', 'is_comleted']
    list_editable = ['is_comleted'] 
admin.site.register(models.Students, AdminStudents)

class AdminGroup(admin.ModelAdmin):
    list_display = ['id', 'name' , 'vaqt', 'acceptance_date', 'is_close']
    list_editable = ['is_close']
admin.site.register(models.Groups, AdminGroup)

class AdminEmployess(admin.ModelAdmin):
    list_display = ['first_name', 'last_name']
admin.site.register(models.Employess, AdminEmployess)

admin.site.register(models.Location)

