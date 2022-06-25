from django.urls import path,include
from . import views

app_name='departments'

urlpatterns = [
    path('',views.departments,name='departments'),
    path('requests',views.requests,name='department_requests'),
    path('items',views.items,name='department_items'),
    path('student_items',views.studentItems,name='student_items'),
    path('item/add',views.newItem,name='new_item'),
    path('item/borrow',views.borrowItem,name='borrow_item'),
    path('search/supervisor/student',views.searchStudent,name='search_student'),
    path('items/clear',views.clearItem,name='clear_item'),
    path('search/student/supervisor', views.searchStudentRequest,
         name='search_student_request'),
]

