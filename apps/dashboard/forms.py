from django import forms
from .models import Employee , Loan , Claim

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


class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = [
            'employee', 'loan_no', 'principal_amount_type', 'loan_type',
            'loan_amount', 'applied_on', 'wef_from', 'deduct_from',
            'monthly_installment', 'closing_balance', 'tenure_months', 'status'
        ]
        widgets = {
            'applied_on': forms.DateInput(attrs={'type': 'date'}),
            'wef_from': forms.DateInput(attrs={'type': 'date'}),
            'deduct_from': forms.DateInput(attrs={'type': 'date'}),
        }

class ClaimForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = ['employee', 'ref_no', 'claim_code', 'claim_type', 'claim_date', 'grand_total']
        widgets = {
            'claim_date': forms.DateInput(attrs={'type': 'date'}),
        }