from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractUser

from .manager import UserManager


ROLE = (
    ("admin", "Admin"),
    ("teacher", "O'qituvchi"),
    ("student", "Talaba"),
)
PAYME_STATE = (
    (1, "To'lov yaratildi. Tasdiqlanishi kutilmoqda"),
    (2, "To'lov amalga muvafaqqiyatli amalga oshirildi"),
    (-1, "To'lov bekor qilindi"),
    (-2, "To'lov tugallangandan keyin qaytarildi."),
)


class User(AbstractUser):
    username = None
    phone = models.CharField(max_length=100, unique=True, null=False, blank=False, verbose_name="Telefon raqami")
    uuid = models.UUIDField(default=uuid4, editable=False)

    first_name = models.CharField(max_length=100, verbose_name="Ism")
    last_name = models.CharField(max_length=100, verbose_name="Familiya")

    city = models.CharField(max_length=100, null=True, blank=True, verbose_name="Viloyat")
    town = models.CharField(max_length=100, null=True, blank=True, verbose_name="Tuman")
    village = models.CharField(max_length=100, null=True, blank=True, verbose_name="Qishloq")
    school = models.CharField(max_length=100, null=True, blank=True, verbose_name="Maktab")

    role = models.CharField(max_length=100, choices=ROLE, verbose_name="Role")
    image = models.ImageField(upload_to="images/users", verbose_name="Rasm", null=True, blank=True)
    balance = models.IntegerField(default=0, verbose_name="Balans")

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = UserManager()
    USERNAME_FIELD = "phone"

    def __str__(self):
        return self.phone
    
    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"


class Group(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, related_name="group_users", blank=True)
    max_members = models.IntegerField(default=10)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def count_members(self):
        return self.members.count()
    

class Invite(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.student.phone
    
class Transaction(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tid = models.CharField(max_length=100)
    state = models.IntegerField(choices=PAYME_STATE)
    amount = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tid

