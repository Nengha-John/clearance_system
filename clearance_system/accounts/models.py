from this import d
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


from .managers import CustomUserManager, RegistrarManager, StudentManager, SuperVisorManager
# Create your models here.


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(
        verbose_name='First Name', name='first_name', max_length=30)
    last_name = models.CharField(
        verbose_name='Last Name', name='last_name', max_length=20)
    email = models.EmailField(verbose_name='Email', name='email', unique=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.first_name + ' ' + self.last_name

    @property
    def getTitle(self):
        try:
            this = self.supervisor
            return 'Supervisor'
        except AttributeError:
            try:
                this = self.registrar
                return 'Registrar'
            except AttributeError:
                return 'Student'

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Registrar(CustomUser):
    staff_number = models.CharField(
        verbose_name='Staff Number', name='stf_number', max_length=50, unique=True)
    is_registrar = models.BooleanField(
        verbose_name='Is Registrar', name='is_registrar', default=True)
    REQUIRED_FIELDS = ['staff_number']

    objects = RegistrarManager()

    @property
    def getTitle(self):
        return 'Registrar'

    class Meta:
        db_table = 'registrar'
        verbose_name = 'Registrar'
        verbose_name_plural = 'Registrars'


class Supervisor(CustomUser):
    staff_number = models.CharField(
        verbose_name='Staff Number', name='stf_number', max_length=50, unique=True)
    is_supervisor = models.BooleanField(
        verbose_name='Is Supervisor', name='is_supervisor', default=True)
    REQUIRED_FIELDS = ['stf_number']

    objects = SuperVisorManager()

    @property
    def getTitle(self):
        return 'Supervisor'

    class Meta:
        db_table = 'supervisors'
        verbose_name = 'Supervisor'
        verbose_name_plural = 'Supervisors'


class Student(CustomUser):
    student_number = models.CharField(
        verbose_name='Student Number', name='std_number', max_length=50, unique=True)
    is_validated = models.BooleanField(
        verbose_name='Validation Status', name='is_validated', default=False)
    sponsor_id = models.ForeignKey(
        to=Supervisor, on_delete=models.PROTECT, null=True, blank=True)
    status = models.BooleanField(
        name='student_status', verbose_name='Cleared', default=False)

    REQUIRED_FIELDS = ['student_number',
                       'course_of_study', 'is_validated', 'registrar']

    objects = StudentManager()

    @property
    def getTitle(self):
        return 'Student'

    class Meta:
        db_table = 'students'
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
