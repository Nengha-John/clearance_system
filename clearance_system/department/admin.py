from django.contrib import admin

from department.models import Department, Items ,StudentItems, StudentCourse, Course

# Register your models here.
class DepartmentAdmin(admin.ModelAdmin):
    model = Department

    list_display = ['dept_name','dept_hod','is_academic']
    list_display_links =['dept_name','dept_hod']
    list_filter = ['dept_name']
    ordering = ('dept_name',)

    fieldsets = (
        ('Item Information:', {'fields': ('dept_name','dept_hod','is_academic',)}),
    )

    add_fieldsets = (
        ('Add Item Information:', {'fields': ('dept_name','dept_hod','is_academic',)}),
    )
    search_field =['dept_name']


class ItemsAdmin(admin.ModelAdmin):
    model = Items

    list_display = ['name','item_dept','price',]
    list_display_links =['name','item_dept',]
    list_filter = ['name']
    ordering = ('name',)

    fieldsets = (
        ('Item Information:', {'fields': ('name','item_dept','price',)}),
    )

    add_fieldsets = (
        ('Add Item Information:', {'fields': ('name','item_dept','price',)}),
    )
    
    search_field =['name']


class StudentItemsAdmin(admin.ModelAdmin):
    model = StudentItems

    list_display = ['student_item','student','borrow_date','return_date','quantity']
    list_display_links =['student_item','student']
    list_filter = ['student']
    ordering = ('student',)

    fieldsets = (
        ('Item Information:', {'fields': ('student_item','student','borrow_date','return_date','quantity',)}),
    )

    add_fieldsets = (
        ('Add Item Information:', {'fields': ('student_item','student','borrow_date','return_date','quantity',)}),
    )
    
    search_field =['student']


class StudentCourseAdmin(admin.ModelAdmin):
    model = StudentCourse

    list_display = ['course','student']
    list_display_links =['course','student']
    list_filter = ['student']
    ordering = ('student',)

    fieldsets = (
        ('Item Information:', {'fields': ('course','student',)}),
    )

    add_fieldsets = (
        ('Add Item Information:', {'fields': ('course','student',)}),
    )
    
    search_field =['student']

class CourseAdmin(admin.ModelAdmin):
    model = Course

    list_display = ['name','course_dept','years']
    list_display_links =['name','course_dept','years']
    list_filter = ['name']
    ordering = ('name',)

    fieldsets = (
        ('Item Information:', {'fields': ('name','course_dept','years',)}),
    )

    add_fieldsets = (
        ('Add Item Information:', {'fields': ('name','course_dept','years',)}),
    )
    
    search_field =['name']


admin.site.register(Department,DepartmentAdmin)
admin.site.register(Items,ItemsAdmin)
admin.site.register(StudentItems,StudentItemsAdmin)
admin.site.register(StudentCourse,StudentCourseAdmin)
admin.site.register(Course,CourseAdmin)
