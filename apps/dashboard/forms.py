from django import forms
from .models import Employee

class EmployeeEditForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'first_name',
            'last_name',
            'company_email',
            'pvt_email',
            'mobile',
            'dob',
            'doj',
            'location',
            'designation',
            'department',
            'manager'
        ]
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'doj': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(EmployeeEditForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
