import json
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as dj_login, logout as dj_logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
import requests
from clearance.models import ClearanceRequests
from clearance.models import ControlNumbers
from department.models import Report
from department.models import StudentItems, Items, Department
from accounts.models import Supervisor, Student,Registrar
from department.models import StudentCourse
from django.contrib import messages


@login_required(login_url='/login')
def home(request):
    if request.user.is_authenticated:
        try:
            if request.user.supervisor.is_supervisor:
                dept = Department.objects.filter(dept_hod=request.user)
                try:
                    items = Items.objects.filter(item_dept=dept[0])
                except:
                    items = ''
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
                pending_items_students = {}
                for req in reqs:
                    student_items = StudentItems.objects.filter(
                        student=req.student, return_date=None)
                    if student_items:
                        pending_items_students[req.student.id] = [
                            item.student_item for item in student_items]
                return render(request, 'dashboard/supervisor.html', {'reqs': reqs, 'items': items, 'dept': dept[0], 'pending_items': pending_items_students})
        except AttributeError:
            try:
                if request.user.registrar.is_registrar:
                    reqs = ClearanceRequests.objects.all()
                    return render(request, 'dashboard/registrar.html', {'reqs': reqs})
            except AttributeError:
                try:
                    ClearanceRequest = ClearanceRequests.objects.filter(
                        student=request.user.student.id)[0]
                    items = StudentItems.objects.filter(
                        student=request.user, return_date=None)
                except:
                    ClearanceRequest = ''
                    items = []
                supervisor = Supervisor.objects.all()
                try:
                    controlNo = ControlNumbers.objects.filter(
                        request=ClearanceRequest)[0]
                except:
                    controlNo = ''
                    pass
                return render(request, 'dashboard/student.html', {'ClearanceRequest': ClearanceRequest, 'items': items, 'supervisors': supervisor, 'controlNo': controlNo})
    return redirect(login)


def login(request):
    form = AuthenticationForm()
    if request.POST:
        std_number = request.POST.get('std-number')
        email = request.POST.get('username')
        payload = json.dumps({'std_number': std_number})
        isStaff = request.POST.get('isStaff')
        if isStaff:
            response = requests.post('http://0.0.0.0:5000/staff', data=payload)
        else:
            response = requests.post(
                'http://0.0.0.0:5000/student', data=payload)
        if response.status_code != 200:
            messages.error(request, 'Failed to verify. Please try again')
            return render(request, 'login.html', {'form': form})
        data = response.json()
        print(data)
        if isStaff and not data['isStaff']:
            messages.error(
                request, 'You are not registred as a staff. Enter a valid Registration Number')
            return render(request, 'login.html', {'form': form})
        if not data['isValid'] and not data['isStaff']:
            messages.error(
                request, 'You are not qualified to attempt clearance')
            return render(request, 'login.html', {'form': form})
        if data['isStaff']:
            print('staff')
            print(email)
            try:
                student = Supervisor.objects.get(email=email)
                print(student)
                pass
            except Supervisor.DoesNotExist:
                try:
                    registrar = Registrar.objects.filter(email=email)
                except Registrar.DoesNotExist:
                    messages.error(
                        request, 'You must be a registred staff member to log in as staff')
                    return render(request, 'login.html', {'form': form})
        elif not data['isStaff'] and not isStaff:
            print('student')
            try:
                print(email)
                student = Student.objects.get(email=email)
                print(student)
                pass
            except Student.DoesNotExist:
                messages.error(
                    request, 'You must be a registred student member to log in as student')
                return render(request, 'login.html', {'form': form})

        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            dj_login(request, user)
            return redirect(home)
        else:
            # messages.error(request,'Invalid email and password')
            return render(request, 'login.html', {'form': form})

    return render(request, 'login.html', {'form': form})


def logout(request):
    if request.method == 'POST':
        dj_logout(request)
        return redirect('login')


def test(request):
    # form = UserCreationForm()
    # form  = DepartmentForm()
    return render(request, 'test.html', {'form': 'success'})


@login_required(login_url='/login')
def registrar(request):
    reqs = ClearanceRequests.objects.filter(status=1)
    pending_items_students = {}
    for req in reqs:
        student_items = StudentItems.objects.filter(
            student=req.student, return_date=None)
        if student_items:
            pending_items_students[req.student.id] = [
                item.student_item for item in student_items]
    return render(request, 'dashboard/registrar.html', {'reqs': reqs, 'pending_items': pending_items_students})


@login_required(login_url='/login')
def registrarCleared(request):
    reqs = ClearanceRequests.objects.filter(status=2)
    return render(request, 'dashboard/registrar.html', {'reqs': reqs})


def report(request):
    if request.POST:
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(email)
        print(message)
        try:
            report = Report.objects.create(
                user=request.user, email=email, message=message)
            messages.info(
                request, 'Your message was submitted successfully. Your feedback helps us improve. Thank you')
            return redirect('/report')
        except BaseException as e:
            messages.error(request, 'An error occured.Please try again'+str(e))
            return render(request, 'dashboard/report.html')
    return render(request, 'dashboard/report.html')
