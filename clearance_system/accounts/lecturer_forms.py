from django import forms
from .user_forms import CustomUserChangeForm,CustomUserCreationForm

from accounts.models import Supervisor

class LecturerCreationForm(CustomUserCreationForm):
    # first_name = forms.CharField(label='First Name',required=True,strip=True)
    # last_name = forms.CharField(label='Last Name',required=True,strip=True)
    # email = forms.EmailField(label='Email',required=True)
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput)
    password2 = forms.CharField(label="Re-enter Password",widget=forms.PasswordInput)
    # staff_number = forms.CharField(label='Staff Number',required=True)

    class Meta:
        model = Supervisor
        # fields = ('password1','password2','stf_number',)
        fields = '__all__'

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords don\'t match')
        return password2
    
    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user


class LecturerChangeForm(CustomUserChangeForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)
    
    class Meta:
        model = Supervisor
        fields =('first_name','last_name','email','stf_number',)