from email.policy import default
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
    first_lastname = models.CharField(max_length=50, verbose_name='Xodimni ismi va familiyasi:')
    acceptance_date = models.DateField(verbose_name='Kelgan sana:', default='')
    pasport = models.CharField(max_length=20 ,verbose_name='Passport raqam:', default='')
    phone_number = models.IntegerField(verbose_name='Telefon raqam:')
    science = models.CharField(max_length=30, verbose_name='Fani:')

    def __str__(self):
        return self.first_lastname

# Guruhlar
class Groups(models.Model):
    name = models.CharField(max_length=100, verbose_name='Guruh nomi:')
    days = models.CharField(max_length=12, choices=Const.days, verbose_name='Dars kunlarini tanlang:')
    vaqt = models.CharField(max_length=50, verbose_name='Dars vaqti:', null=True)
    acceptance_date = models.DateField(verbose_name='Ochilgan sana:')
    duration = models.IntegerField(verbose_name='Dars davomiyligi: ')
    teacher = models.ForeignKey(Employess, models.CASCADE, verbose_name='Biriktirilgan o\'qituvchi')
    price = models.DecimalField(decimal_places=2, max_digits=50, verbose_name='Kursni narxi:')
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
    image = models.ImageField(verbose_name='O\'quvchini rasmi:', default=' ')
    birthday = models.DateField(verbose_name='Tug\'ilgan sana:')
    phone_number = models.IntegerField(verbose_name='Telefon raqami:')
    email = models.CharField(max_length=100, verbose_name='Email manzili:')
    shartnoma_raqami = models.CharField(max_length=30, verbose_name='Shartnoma raqami:')
    PINFL_number = models.CharField(max_length=30, verbose_name='PINFL/Passport raqami:')
    region = models.CharField(max_length=31, choices=Const.regions, verbose_name='Viloyatni tanlang:')
    district = models.CharField(max_length=35, verbose_name="Tuman va manzilni kiriting:")
    freedom = models.DecimalField(max_digits=50, decimal_places=2, verbose_name='Imtiyozi:', default=0)
    is_comleted = models.BooleanField(default=False, verbose_name='Tugatish holati')
    username = models.CharField(max_length=6, blank=True, null=True)
    parol = models.CharField(max_length=15, blank=True, null=True)

    def get_price_money(self): # To'lanishi kerak bo'lgan summa
        price_money = self.acceptance_group.price - self.freedom
        return price_money

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

# Payments
class Payments(models.Model):
    student = models.ForeignKey(Students, models.CASCADE, verbose_name='O\'quvchini tanlang:')
    from_period = models.DateField()
    do_period = models.DateField()
    price = models.DecimalField(max_digits=50, decimal_places=2, verbose_name='Narxi')
    freedom = models.DecimalField(max_digits=50, decimal_places=2, verbose_name='Imtiyoz:')
    price_money = models.DecimalField(max_digits=50, decimal_places=2, verbose_name='To\'lanishi kerak:')
    status = models.BooleanField(default='False', verbose_name='Holat')

    def __str__(self):
        return f"{self.students} || {self.from_period}&{self.do_period}"

    def mark_status(self):
        self.status = True
        self.save()

    
     