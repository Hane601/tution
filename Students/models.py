from django.db import models
from django.contrib.auth.hashers import make_password

class Member(models.Model):
  student_id = models.CharField(max_length=7, unique=True)
  firstname = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)
  phone = models.CharField(max_length=10)
  Mahaoya = models.BooleanField(default=False)
  Kakirihena = models.BooleanField(default=False)
  Maths = models.BooleanField(default=False)
  English = models.BooleanField(default=False)
  Science = models.BooleanField(default=False)
  Sinhala = models.BooleanField(default=False)
  Buddhism = models.BooleanField(default=False)
  History = models.BooleanField(default=False)
  year = models.CharField(max_length=4)
  qr = models.ImageField(upload_to='qrcodes/', blank=True, null=True)

  def __str__(self):
        return f"{self.firstname} {self.lastname} {'\u00A0\u00A0\u00A0'}{'\u00A0\u00A0\u00A0'}{'\u00A0\u00A0\u00A0'}{'\u00A0\u00A0\u00A0'}{self.student_id}"  



class register(models.Model):
    dates = models.DateField()

    def __str__(self):
        return f"{self.dates}"

class student(models.Model):
    main = models.ForeignKey(register, related_name='students', on_delete=models.CASCADE)
    student_id = models.CharField(max_length=7, null=True)
    name = models.CharField(max_length=100, null = True)
    specific_class = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Tutor(models.Model):
    username = models.CharField(max_length=100, unique=True)
    contact = models.CharField(max_length=10)
    password = models.CharField(max_length=128)
    English = models.BooleanField(default=False)
    Maths = models.BooleanField(default=False)
    Science = models.BooleanField(default=False)
    Sinhala = models.BooleanField(default=False)
    Buddhism = models.BooleanField(default=False)
    History = models.BooleanField(default=False)
    Mahaoya = models.BooleanField(default=False)
    Kakirihena = models.BooleanField(default=False)  

    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)  # Hash before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username



