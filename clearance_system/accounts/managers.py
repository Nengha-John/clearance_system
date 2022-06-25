from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(
        self,
        first_name,
        last_name,
        email,password
        ):
        user = self.model(
            first_name = first_name,
            last_name = last_name,
            email = email
        )
        user.set_password(password)
        user = user.save()
        return user

    def create_superuser(self, **extra_fields):
        superuser = self.create_user(**extra_fields)
        superuser.is_superuser = True
        superuser = superuser.save()
        return superuser


class RegistrarManager(CustomUserManager):
    def create_user(self, first_name, last_name, email, password,staff_number):
        user = self.model(
            first_name,last_name,email,staff_number
        )
        user.is_registrar = True
        user.set_password(password)
        user = user.save()
        return user

class SuperVisorManager(CustomUserManager):
    def create_user(self, first_name, last_name, email, password,staff_number):
        user = self.model(
            first_name,last_name,email,staff_number
        )
        user.set_password(password)
        user.is_supervisor = True
        user = user.save()
        return user

class StudentManager(CustomUserManager):
    def create_user(self, first_name, last_name, email, password,student_number,course_of_student,is_validated,registrar):
        user = self.model(first_name, last_name, email,student_number,course_of_student,is_validated,registrar)
        user.set_password(password)
        user = user.save()
        return user