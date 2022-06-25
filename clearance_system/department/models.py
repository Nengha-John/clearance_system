from django.db import models
from accounts.models import Supervisor,Student

# Create your models here.
class Department(models.Model):
    dept_name = models.CharField(verbose_name='Department Name',name='dept_name',max_length=100)
    dept_head = models.ForeignKey(to=Supervisor,name='dept_hod',verbose_name='HOD',on_delete=models.PROTECT)
    is_academic = models.BooleanField(name='is_academic',verbose_name='Is Academic',default=False)
    

    def __str__(self) -> str:
        return self.dept_name + ' ' + str(self.dept_hod)
    
    class Meta:
        db_table = 'departments'
        verbose_name = 'Department'
        verbose_name_plural = "Departments"

class Items(models.Model):
    name = models.CharField(verbose_name='Item Name',name='name',max_length=100)
    department = models.ForeignKey(to=Department,on_delete=models.PROTECT,name='item_dept',verbose_name='Department')
    price = models.IntegerField(verbose_name='price',name='price',default=0)
    Items = models.ManyToManyField(to=Student,through='StudentItems',related_name='student_items')

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = "Items"

class Course(models.Model):
    course_name = models.CharField(verbose_name='Course Name',name='name',max_length=200)
    dept = models.ForeignKey(to=Department,name='course_dept', on_delete=models.PROTECT)
    years_of_study = models.IntegerField(name='years',verbose_name='Years of Study')

    def __str__(self) -> str:
        return self.name + str(self.course_dept)

    class Meta:
        db_table = 'courses'
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'


class StudentCourse(models.Model):
    course = models.ForeignKey(to=Course,name='course',on_delete=models.PROTECT)
    student = models.OneToOneField(to=Student,name='student',on_delete=models.PROTECT,unique=True)
    created = models.DateField(name='create_date',verbose_name='Createdd On', auto_now_add=True)

    class Meta:
        db_table = 'student_courses'
        verbose_name = 'Student Course'
        verbose_name_plural = 'Student Courses'


class StudentItems(models.Model):
    item = models.ForeignKey(to=Items,on_delete=models.PROTECT,name='student_item')
    student = models.ForeignKey(to=Student,on_delete=models.PROTECT,name='student')
    borrowed_on = models.DateField(name='borrow_date',verbose_name='Borrowed On', auto_now_add=True)
    returned_on = models.DateField(name='return_date',verbose_name='Returned On', null=True,blank=True)
    quantity = models.IntegerField(name='quantity',verbose_name='Quantity')

    @property
    def totalCost(self):
        return self.quantity * self.student_item.price

    class Meta:
        verbose_name = 'Student Item'
        verbose_name_plural = "Student Items"



