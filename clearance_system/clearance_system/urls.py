"""clearance_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views
import clearance
app_name = 'home'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name='home'),
    path('report',views.report,name='report'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('test/',views.test),
    path('requests/',include('clearance.urls')),
    path('department/',include('department.urls')),
    path('registrar/',views.registrar,name='registrar'),
    path('registrar/cleared/',views.registrarCleared,name='registrar_cleared')
]
