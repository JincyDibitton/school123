from django import forms
from django.forms.widgets import PasswordInput, EmailInput
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model,authenticate
from .models import Student,Courses,Department

User = get_user_model()

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user


class UserRegistrationForm(forms.Form):
    username            = forms.CharField()
    email               = forms.EmailField(widget=EmailInput)
    password            = forms.CharField(widget=PasswordInput)
    password2           = forms.CharField(label='Confirm password', widget=PasswordInput)

    def clean_username(self):
        username        = self.cleaned_data.get('username')
        qs              = User.objects.filter(username=username)
        
        print("checking if user exists")
        if qs.exists():
            raise forms.ValidationError("Username is taken.")

        print("returning username")
        return username

    def clean_email(self):
        email           = self.cleaned_data.get('email')
        qs              = User.objects.filter(email=email)
        
        print("checking if user exists")
        if qs.exists():
            raise forms.ValidationError("Email already exists.")

        print("returning email")
        return email


    def clean(self):
        cleaned_data    = super(UserRegistrationForm, self).clean()
        print("clean is called")
        password        = cleaned_data.get("password")
        password2       = cleaned_data.get("password2")

        if password != password2:
            print("passwords did not match")
            raise forms.ValidationError("Passwords must match.")
        
        print("returning cleaned_data")
        return cleaned_data


purpose = (
    ("1", "Enquiry"),
    ("2", "Place Order"),
    ("3", "Return"),
    ("4", "Feedback"),
    ("5", "Queries"),
)
materials_choices = (
                    ('Notebook', 'Notebook'), 
                    ('Pen', 'Pen'),
                    ('Exam Papers', 'Exam Papers'),
                    ('Books', 'Books'))
gender_choices = (('M', 'Male'), ('F', 'Female'))

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'

        
         
        widgets = { 'first_name': forms.TextInput(attrs={ 'class': 'form-control' }),
                    'last_name': forms.TextInput(attrs={ 'class': 'form-control' }),
                        'dob': forms.DateInput(
                    attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)', 'class': 'form-control'}
                ),
                        'address':forms.TextInput(attrs={ 'class': 'form-control' }),
                        'email': forms.EmailInput(attrs={ 'class': 'form-control' }),
                        
                        'age': forms.TextInput(attrs={ 'class': 'form-control' }),
                        'address': forms.TextInput(attrs={ 'class': 'form-control' }),
                        'department': forms.Select(attrs={'class': 'form-control'}),
                        'courses': forms.Select(attrs={'class': 'form-control'}),
                        'phoneNumber': forms.TextInput(attrs={'class': 'form-control'}),
                        
                        'gender': forms.RadioSelect
                        
                    
            } 
            
        purpose = forms.ChoiceField(choices=purpose)
        materials = forms.ChoiceField(choices=materials_choices)
            
            
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['courses'].queryset = Courses.objects.none()

        if 'department' in self.data:
            try:
                department_id = int(self.data.get('department'))
                self.fields['courses'].queryset = Courses.objects.filter(department_id=department_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['courses'].queryset = self.instance.department.courses_set.order_by('name')        