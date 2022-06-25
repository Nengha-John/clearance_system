from django.urls import path, include
from . import views
app_name = 'clearance'

urlpatterns = [
    path('', views.clearances, name='request'),
    path('controlno/', views.controlNo, name='control_number'),
    path('registrar/clear/', views.clearStudent, name='registrar_clear'),
    path('search/student', views.searchStudent, name='search_student'),
]
