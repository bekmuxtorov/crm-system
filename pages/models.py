from django.db import models
from .const import Const

# Create your models here.
class Location(models.Model):
    regions = models.CharField(max_length=31, choices=Const.regions, verbose_name="Viloyatni tanlang:")
    district = models.CharField(max_length=35, verbose_name="Tumanni kiriting:")

    def __str__(self):
        return f"{self.district}, {dict(Const.regions)}"

# Xodimlar
class Employess(models.Model): 
    first_name = models.CharField(max_length=30, verbose_name='Xodimni ismi:')
    last_name = models.CharField(max_length=30, verbose_name='Xodimni familiyasi:')

    def __str__(self):
        return self.first_name

# Guruhlar
class Groups(models.Model):
    name = models.CharField(max_length=100, verbose_name='Guruh nomi:')
    vaqt = models.CharField(max_length=50, verbose_name='Dars vaqti:', null=True)
    acceptance_date = models.DateField(verbose_name='Ochilgan sana:')
    teacher = models.ForeignKey(Employess, models.CASCADE, verbose_name='Biriktirilgan o\'qituvchi')
    is_close = models.BooleanField(default=False, verbose_name='Tugatish holati')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return ("/groups")


# Studentlar ma'lumotlarini saqlash uchun SQLITE ma'lumotlar ombori
class Students(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='O\'quvchini ismi va familiyasi: ')
    acceptance_date = models.DateField(verbose_name='Qabul qilingan sana:')
    acceptance_group = models.ForeignKey(Groups, models.CASCADE, verbose_name='Qabul qilingan guruh:')
    birthday = models.DateField(verbose_name='Tug\'ilgan sana:')
    phone_number = models.IntegerField(verbose_name='Telefon raqami:')
    email = models.CharField(max_length=100, verbose_name='Email manzili:')
    shartnoma_raqami = models.CharField(max_length=30, verbose_name='Shartnoma raqami:')
    PINFL_number = models.CharField(max_length=30, verbose_name='PINFL/Passport raqami:')
    region = models.CharField(max_length=31, choices=Const.regions, verbose_name='Viloyatni tanlang:')
    district = models.CharField(max_length=35, verbose_name="Tuman va manzilni kiriting:")
    is_comleted = models.BooleanField(default=False, verbose_name='Tugatish holati')

    def get_date(self):
        acceptance_date = self.acceptance_date
        return acceptance_date.strftime("%d/%m/%Y")

    def __str__(self):
        return self.first_name

    def get_absolute_url(self):
        return ("/students")

    def mark_as_completed(self):
        self.is_comleted = True
        self.save()
    