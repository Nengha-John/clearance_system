from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .user_forms import CustomUserChangeForm,CustomUserCreationForm
from .models import CustomUser,Registrar,Student, Supervisor
from .registrar_forms import RegistrarChangeForm,RegistrarCreationForm
from  .student_forms import StudentChangeForm,StudentCreationForm
from .lecturer_forms import LecturerChangeForm, LecturerCreationForm

# Register your models here.
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ['first_name','last_name','email']
    list_display_links =['first_name','last_name']
    list_filter = ['first_name']
    ordering = ('first_name',)
    # fields = ['phone', 'password1','password2','first_name','last_name','dob','address','email']
    fieldsets = (
        ('Personal info', {'fields': ('first_name','last_name','email',)}),
    )

    add_fieldsets = (
        ('User Information', {'fields': ('email', 'password1','password2',)}),
        ('Personal Information', {'fields': ('first_name','last_name',)}),
    )

    search_field =['email']


class RegistrarAdmin(CustomUserAdmin):
    add_form = RegistrarCreationForm
    form = RegistrarChangeForm
    model = Registrar

    list_display = ['first_name','last_name','email','stf_number']
    list_display_links =['first_name','last_name']
    list_filter = ['first_name']
    ordering = ('first_name',)
    # fields = ['phone', 'password1','password2','first_name','last_name','dob','address','email']
    fieldsets = (
        ('Personal info', {'fields': ('first_name','last_name','email',)}),
    )

    add_fieldsets = (
        ('User Information', {'fields': ('email', 'password1','password2',)}),
        ('Personal Information', {'fields': ('first_name','last_name','stf_number')}),
    )

    search_field =['email']


class SupervisorAdmin(CustomUserAdmin):
    add_form = LecturerCreationForm
    form = LecturerChangeForm
    model = Supervisor

    list_display = ['first_name','last_name','email','stf_number']
    list_display_links =['first_name','last_name']
    list_filter = ['first_name']
    ordering = ('first_name',)
    # fields = ['phone', 'password1','password2','first_name','last_name','dob','address','email']
    fieldsets = (
        ('Personal info', {'fields': ('first_name','last_name','email',)}),
    )

    add_fieldsets = (
        ('User Information', {'fields': ('email', 'password1','password2',)}),
        ('Personal Information', {'fields': ('first_name','last_name','stf_number')}),
    )

    search_field =['email']



class StudentAdmin(CustomUserAdmin):
    add_form = StudentCreationForm
    form = StudentChangeForm
    model = Student

    list_display = ['first_name','last_name','email','std_number','is_validated','sponsor_id']
    list_display_links =['first_name','last_name']
    list_filter = ['first_name']
    ordering = ('first_name',)
    # fields = ['phone', 'password1','password2','first_name','last_name','dob','address','email']
    fieldsets = (
        ('Personal info', {'fields': ('first_name','last_name','email',)}),
        ('Academic info', {'fields': ('std_number','is_validated','sponsor_id',)}),
    )

    add_fieldsets = (
        ('User Information', {'fields': ('email', 'password1','password2',)}),
        ('Personal Information', {'fields': ('first_name','last_name',)}),
        ('Academic info', {'fields': ('std_number','is_validated','sponsor_id',)}),
    )

    search_field =['email']



admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Registrar, RegistrarAdmin)
admin.site.register(Supervisor, SupervisorAdmin)
admin.site.register(Student, StudentAdmin)
