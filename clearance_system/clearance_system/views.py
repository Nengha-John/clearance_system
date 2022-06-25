from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as dj_login,logout as dj_logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from clearance.models import ClearanceRequests
from clearance.models import ControlNumbers
from department.models import StudentItems, Items,Department
from accounts.models import Supervisor,Student
from department.models import StudentCourse


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
                    student_items = StudentItems.objects.filter(student=req.student,return_date=None)
                    if student_items:
                        pending_items_students[req.student.id] = [item.student_item for item in student_items]
                return render(request,'dashboard/supervisor.html',{'reqs': reqs,'items': items,'dept':dept[0],'pending_items':pending_items_students})
        except AttributeError:
            try:
                if request.user.registrar.is_registrar:
                    reqs = ClearanceRequests.objects.all()
                    return render(request,'dashboard/registrar.html',{'reqs': reqs})
            except AttributeError:
                try:
                    ClearanceRequest = ClearanceRequests.objects.filter(student=request.user.student.id)[0]
                    items = StudentItems.objects.filter(student=request.user,return_date=None)
                except:
                    ClearanceRequest = ''
                    items = []
                supervisor = Supervisor.objects.all()
                try:
                    controlNo = ControlNumbers.objects.filter(request=ClearanceRequest)[0]
                except:
                    controlNo = ''
                    pass
                return render(request,'dashboard/student.html',{'ClearanceRequest': ClearanceRequest,'items': items,'supervisors': supervisor,'controlNo': controlNo})
    return redirect(login)


def login(request):
    if request.POST:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            dj_login(request,user)
            return redirect(home)
        else:
            # messages.error(request,'Invalid email and password')
            return render(request,'login.html',{'form':form})
    form = AuthenticationForm()
    
    return render(request,'login.html',{'form':form})

def logout(request):
    if request.method == 'POST':
        dj_logout(request)
        return redirect('login')


def test(request):
    # form = UserCreationForm()
    # form  = DepartmentForm()
    return render(request,'test.html',{'form': 'success'})

@login_required(login_url='/login')
def registrar(request):
    reqs = ClearanceRequests.objects.filter(status=1)
    pending_items_students = {}
    for req in reqs:
        student_items = StudentItems.objects.filter(student=req.student,return_date=None)
        if student_items:
            pending_items_students[req.student.id] = [item.student_item for item in student_items]
    return render(request,'dashboard/registrar.html',{'reqs': reqs,'pending_items':pending_items_students})

@login_required(login_url='/login')
def registrarCleared(request):
    reqs = ClearanceRequests.objects.filter(status=2)
    return render(request,'dashboard/registrar.html',{'reqs': reqs})

