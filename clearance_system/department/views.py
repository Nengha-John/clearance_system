from ntpath import join
from django.http import HttpResponse
from django.shortcuts import redirect, render
import datetime
from accounts.models import Student
from .models import Department, Items, StudentCourse, StudentItems
from .forms import ItemsForm, StudentItemsForm
from clearance.models import ClearanceRequests
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.defaulttags import register
from department.models import StudentCourse, Course
import requests as http


@register.filter
def get_item(dictionary, key):
    if type(dictionary.get(key)) == type([]):
        items = [item.name for item in dictionary.get(key)]
        val = ', '.join(items) + ' not returned'
        return val
    return dictionary.get(key)


@register.filter
def get_tuition_status(std_num):
    print(std_num)
    try:
        feeStat = http.get(
            'http://0.0.0.0:5000/student/{}'.format(std_num)).json()
        if feeStat['status']:
            return "Fully Paid"
        else:
            return "Due: {}".format(feeStat['due_amount'])
    except BaseException as e:
        return 'Not Found'


# Create your views here.


@login_required(login_url='/login')
def departments(request):
    course = StudentCourse.objects.get(student=request.user)
    deps = []
    academic_deps = Department.objects.filter(pk=course.course.course_dept.id)
    non_academic = Department.objects.filter(is_academic=False)

    for dep in academic_deps:
        deps.append(dep)
    for dep in non_academic:
        deps.append(dep)
    try:
        items = StudentItems.objects.filter(
            student=request.user, return_date=None)
    except StudentItems.DoesNotExist:
        items = []
    overdue_deps = [item.student_item.item_dept.id for item in items]
    return render(request, 'dashboard/departments.html', {'deps': deps, 'items': items, 'overdue': overdue_deps})


@login_required(login_url='/login')
def requests(request):
    print(request.user)
    dept = Department.objects.filter(dept_hod=request.user)
    items = Items.objects.filter(item_dept=dept[0])
    all_reqs = ClearanceRequests.objects.all()
    reqs = []
    if dept[0].is_academic:
        for req in all_reqs:
            std = Student.objects.get(pk=req.student.id)
            course = StudentCourse.objects.filter(student=std)[0]
            if course.course.course_dept.id == dept[0].id:
                reqs.append(req)
    else:
        reqs = ClearanceRequests.objects.all()
    print(reqs)
    pending_items_students = {}
    for req in reqs:
        print(type(req))
        student_items = StudentItems.objects.filter(
            student=req.student, return_date=None)
        if student_items:
            pending_items_students[req.student.id] = [
                item.student_item for item in student_items]
    return render(request, 'dashboard/supervisor_requests.html', {'reqs': reqs, 'items': items, 'dept': dept[0], 'pending_items': pending_items_students})


@login_required(login_url='/login')
def items(request):
    dept = Department.objects.filter(dept_hod=request.user)
    items = Items.objects.filter(item_dept=dept[0])
    return render(request, 'dashboard/supervisor_items.html', {'items': items})


@login_required(login_url='/login')
def studentItems(request):
    if request.POST:
        return HttpResponse('Post items')
    else:
        students = []
        dept = Department.objects.filter(dept_hod=request.user.id)[0]
        if dept.is_academic:
            courses = Course.objects.filter(course_dept=dept)
            print(courses)
            for course in courses:
                studs = StudentCourse.objects.filter(course=course)
                for stud in studs:
                    print(stud)
                    students.append(stud.student)
            std_items = [item for item in StudentItems.objects.all()
                         if item.student in students and item.student_item.item_dept == dept]
        else:
            std_items_all = StudentItems.objects.all()
            std_items = []
            for item in std_items_all:
                if item.student_item.item_dept.id == dept.id:
                    std_items.append(item)
            students = Student.objects.all()
        for itm in std_items:
            print(itm.student_item)
        dept_items = Items.objects.filter(item_dept=dept.id)

        return render(request, 'dashboard/supervisor_student.html', {'items': std_items, 'students': students, 'dept_items': dept_items})


@login_required(login_url='/login')
def newItem(request):
    if request.POST:
        name = request.POST.get('name')
        price = request.POST.get('price')
        dept = Department.objects.filter(dept_hod=request.user.supervisor)[0]
        item = Items.objects.create(name=name, item_dept=dept, price=price)
        item = item.save()
        messages.success(request, 'Item added successfully')
        return redirect('/department/items')


@login_required(login_url='/login')
def borrowItem(request):
    if request.POST:
        studentItemForm = StudentItemsForm(data=request.POST)
        if studentItemForm.is_valid():
            item = studentItemForm.save()
            messages.success(request, 'Record Saved succesfully')
            return redirect('/department/student_items')
        else:
            messages.error(request, 'An error occured')
            return redirect('/department/student_items')


@login_required(login_url='/login')
def searchStudent(request):
    if request.POST:
        query = request.POST.get('query')
        dept = Department.objects.filter(dept_hod=request.user)
        student = Student.objects.filter(std_number=query.replace(' ', ''))
        if student:
            student = student[0]
        else:
            return redirect('/search/supervisor/student')
        itemList = StudentItems.objects.filter(student=student[0])
        items = []
        for item in itemList:
            if item.student_item.item_dept == dept:
                items.append(item)
        return render(request, 'dashboard/supervisor_student.html', {'items': items})


@login_required(login_url='login/')
def clearItem(request):
    if request.POST:
        stdItem = request.POST.get('std_item')
        item = StudentItems.objects.get(pk=stdItem)
        item.return_date = datetime.date.today()
        item.save()
        return redirect('/department/student_items')


@login_required(login_url='/login')
def searchStudentRequest(request):
    if request.POST:
        query = request.POST.get('query')
        student = Student.objects.filter(std_number=query.replace(' ', '-'))[0]
        dept = Department.objects.filter(dept_hod=request.user)[0]
        if dept.is_academic:
            stdCourse = StudentCourse.objects.filter(student=student)
            if not stdCourse.course.dept == dept:
                return redirect('/supervisor/requests')
            else:
                student = ''
        reqs = ClearanceRequests.objects.filter(student=student)
        pending_items_students = {}
        for req in reqs:
            student_items = StudentItems.objects.filter(
                student=req.student, return_date=None)
            if student_items:
                pending_items_students[req.student.id] = [
                    item.student_item for item in student_items]
        return render(request, 'dashboard/supervisor_requests.html', {'reqs': reqs, 'pending_items': pending_items_students})
