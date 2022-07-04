from random import Random
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from accounts.models import Student
from accounts.models import Supervisor
from department.models import Course, Department, StudentCourse
from department.models import StudentItems
from .models import ClearanceRequests
from .forms import ClearanceRequestForm
from django.contrib import messages
from .models import ControlNumbers

# Create your views here.


@login_required(login_url='/login')
def clearances(request):
    if request.POST:
        student_id = request.POST.get('student')
        supervisor_id = request.POST.get('supervisor')
        try:
            supervisor = Supervisor.objects.get(pk=supervisor_id)
        except Supervisor.DoesNotExist:
            messages.error(request, 'An error occured. Please try again')
        user = Student.objects.get(pk=request.user.id)
        user.sponsor_id = supervisor
        user.save()
        course = StudentCourse.objects.filter(student=user)[0]
        dept = Department.objects.get(pk=course.course.course_dept.id)
        ClearanceRequest = ClearanceRequests.objects.filter(student=student_id)

        if ClearanceRequest:
            messages.error(request, 'You already have a pending request')
        else:
            ClearanceRequest = ClearanceRequests(student=request.user.student)
            if ClearanceRequest:
                ClearanceRequest = ClearanceRequest.save()
                messages.success(request, 'Request Submitted Successfully')
            else:
                messages.error(request, 'An error occured please try again')
        return render(request, 'dashboard/student.html', {'ClearanceRequest': [ClearanceRequest], 'supervisors': supervisor, 'course': course, 'dept': dept})


@login_required(login_url='/login')
def controlNo(request):
    if request.POST:
        clearanceRequestId = request.POST.get('request')
        studentItems = StudentItems.objects.filter(student=request.user.id)
        items = StudentItems.objects.filter(
            student=request.user, return_date=None)
        try:
            supervisor = Supervisor.objects.get(
                pk=request.user.student.sponsor_id)
        except Supervisor.DoesNotExist:
            supervisor = ''
        clearanceRequest = ClearanceRequests.objects.get(pk=clearanceRequestId)
        try:
            testControlNum = ControlNumbers.objects.filter(
                request=clearanceRequest)
            if testControlNum:
                messages.info(
                    request, 'A control number already exist for this request')
                # return r(request,'dashboard/student.html',{'ClearanceRequest': clearanceRequest,'items': items,'supervisors': supervisor,'controlNo':testControlNum})
                return redirect('home')
        except ControlNumbers.DoesNotExist:
            pass
        control_no = Random().randrange(start=1000000000, stop=100000000000000)
        print(control_no)
        amount = 0
        if studentItems:
            for item in studentItems:
                amount += item.student_item.price * item.quantity
        controlNo = ControlNumbers.objects.create(
            request=clearanceRequest, control_no=control_no, amount=amount)
        controlNo = controlNo.save()
    return render(request, 'dashboard/student.html', {'ClearanceRequest': clearanceRequest, 'items': items, 'supervisors': supervisor, 'controlNo': controlNo})


@login_required(login_url='login/')
def clearStudent(request):
    if request.POST:
        reqId = request.POST.get('req_id')
        try:
            studentRequest = ClearanceRequests.objects.get(pk=reqId)
            try:
                studentItems = StudentItems.objects.filter(
                    student=studentRequest.student, return_date=None)
                print(studentItems)
                if studentItems:
                    messages.error(
                        request, 'This request has pending clearances')
                    return redirect('/')
            except StudentItems.DoesNotExist:
                pass
        except ClearanceRequests.DoesNotExist:
            messages.error(request, 'An error occured. Please try again')
            return redirect('/')
        studentRequest.status = 2
        studentRequest.save()
        student = Student.objects.get(pk=studentRequest.student.id)
        student.student_status = 1
        student.save()
        return redirect('registrar')


@login_required(login_url='/login')
def searchStudent(request):
    if request.POST:
        query = request.POST.get('query')
        student = Student.objects.filter(std_number=query.replace(' ', '-'))
        if student:
            student = student[0]
        else:
            return redirect('/search/student')
        reqs = ClearanceRequests.objects.filter(student=student)
        pending_items_students = {}
        for req in reqs:
            student_items = StudentItems.objects.filter(
                student=req.student, return_date=None)
            if student_items:
                pending_items_students[req.student.id] = [
                    item.student_item for item in student_items]
        return render(request, 'dashboard/registrar.html', {'reqs': reqs, 'pending_items': pending_items_students})
