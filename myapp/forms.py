from django import forms
from django.forms import ModelForm
from myapp.models import Order, Review, Student


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['reviewer', 'course', 'rating', 'comments']
        widgets = {'course': forms.RadioSelect}
        labels = {'reviewer': u'please enter a valid email',
                  'rating': u'Rating : An integer between 1(worst) and 5(best)'}


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['courses', 'Student', 'order_status']
        widgets = {'courses': forms.CheckboxSelectMultiple(), 'order_type': forms.RadioSelect}
        labels = {'Student': u'Student Name'}


class SearchForm(forms.Form):
    LENGTH_CHOICES = [
        (8, '8 Weeks'),
        (10, '10 Weeks'),
        (12, '12 Weeks'),
        (14, '14 Weeks'),
    ]

    name = forms.CharField(max_length=100, required=False, label='Student Name')
    length = forms.TypedChoiceField(widget=forms.RadioSelect, choices=LENGTH_CHOICES, coerce=int, required=False, label='Preferred course duration:')
    max_price = forms.IntegerField(min_value=0,label='Maximum Price')


class RegisterForm(ModelForm):
    class Meta:
        model = Student
        fields = ('username', 'email', 'password','first_name','last_name', 'level','province','registered_courses','interested_in','student_image')
        required = ('username', 'email', 'password','first_name','level','province')
        widgets = {
            'password': forms.PasswordInput
        }
class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_image']
        labels = {'student_image': 'Upload Image '}


class ForgotPasswordForm(forms.Form):
    email = forms.CharField(max_length=100, required=True, label='Email')


