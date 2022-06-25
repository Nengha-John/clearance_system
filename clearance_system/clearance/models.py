from urllib import request
from django.db import models
from accounts.models import Student

# Create your models here.
class ClearanceRequests(models.Model):
    class RequestStatus(models.IntegerChoices):
        SUBMITTED = 0
        REVIEW = 1
        CLEARED = 2
        
    student = models.ForeignKey(to=Student,on_delete=models.PROTECT,name='student')
    requested_on = models.DateTimeField(name='requested_on',verbose_name='Date of Request',auto_now_add=True)
    status = models.IntegerField(name='status',verbose_name='Status',default=1,choices=RequestStatus.choices)
    

    def getControlNo(self):
        return ControlNumbers.objects.filter(request_id=self.id)

    def __str__(self) -> str:
        return str(self.student)

    
    class Meta:
        verbose_name = 'Request'
        verbose_name_plural = 'Requests'


class ControlNumbers(models.Model):
    control_no = models.CharField(name='control_no',verbose_name='Control Number',unique=True,max_length=14)
    request = models.OneToOneField(to=ClearanceRequests,on_delete=models.PROTECT,name='request',unique=True)
    amount_payable = models.IntegerField(name='amount',verbose_name='Amount Payable')
    created = models.DateTimeField(name='created',verbose_name='Student', auto_now_add=True)

    def __str__(self) -> str:
        return str(self.request) + " " + str(self.amount)

    
    class Meta:
        verbose_name = 'Control Number'
        verbose_name_plural = 'Control Numbers'