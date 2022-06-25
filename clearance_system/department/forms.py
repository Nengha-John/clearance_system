from django import forms
from department.models import Department, Items, StudentItems

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['dept_name','dept_hod']


class ItemsForm(forms.ModelForm):
    class Meta:
        model = Items
        fields = ['name','item_dept','price']


class StudentItemsForm(forms.ModelForm):
    class Meta:
        model = StudentItems
        fields = ['student_item','student','quantity']