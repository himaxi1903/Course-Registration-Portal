# Create your views here.
# Import necessary classes
from datetime import datetime

from django.core import mail
from django.utils import timezone
from urllib.parse import urlencode
from time import time, ctime
from django.http import HttpResponse, HttpResponseRedirect, response
from .models import Topic, Course, Student, Order
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from .forms import SearchForm, OrderForm, ReviewForm, RegisterForm, ForgotPasswordForm, ImageUploadForm
# Import necessary classes and models
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail


# Create your views here.
def index(request):
    top_list = Topic.objects.all().order_by('id')[:10]
    return render(request, 'myapp/index.html', {'top_list': top_list})


# def about(request):
#   return HttpResponse("This is an E-learning Website! Search our Topics to find all available Courses.")

def about(request):
    if 'about_visits' in request.COOKIES:
        num_of_visits = int(request.COOKIES['about_visits'])
        num_of_visits += 1
    else:
        num_of_visits = 1

    response = render(request, 'myapp/about.html', {'total_visits': num_of_visits})
    response.set_cookie('about_visits', num_of_visits, max_age=300)
    return response
    # response = HttpResponse()
    # heading = '<p>' + 'This is an E-learning Website! Search our Topics to find all available Courses.' + '</p>'
    # response.write(heading)


# return render(request, 'myapp/about.html', {'heading': heading})




def detail(request, topic_id):
    topic_name = Topic.objects.all()
    topic = get_object_or_404(topic_name, id=topic_id)
    course_list = Course.objects.filter(topic=topic)
    return render(request, 'myapp/detail.html', {'topic': topic, 'course_list': course_list})


# def detail(request, topic_id):
#
#     topic_category = get_object_or_404(Topic, id=topic_id)
#     topic = Topic.objects.get(id=topic_id).name
#     course_list = Course.objects.filter(topic__name=topic)
#     return render(request, 'myapp/detail0.html', {'topic_category': topic_category, 'topic_name': topic, 'course_list': course_list})


def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            courses = form.cleaned_data['courses']
            order = form.save(commit=False)
            student = order.Student
            status = order.order_status
            order.save()
            if status == 1:
                for c in order.courses.all():
                    student.registered_courses.add(c)
                form.save()
                return render(request, 'myapp/order_response.html', {'courses': courses, 'order': order})
            elif status == 0:
                for c in order.courses.all():
                    student.registered_courses.remove(c)
                form.save()
                return render(request, 'myapp/order_response.html', {'courses': courses, 'order': order})
            else:
                for c in order.courses.all():
                    student.registered_courses.add(c)
                form.save()
                return render(request, 'myapp/order_response.html', {'courses': courses, 'order': order})

        else:
            return render(request, 'myapp/place_order.html', {'form': form})
    else:
        form = OrderForm()
        return render(request, 'myapp/place_order.html', {'form': form})


def review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            if (rating >= 1 and rating <= 5):
                review = form.save()
                course = Course.objects.get(id=review.course.id)
                course.num_reviews += 1
                course.save()
                return redirect('myapp:index')
            else:
                return HttpResponse('You must enter rating between 1 and 5')
                # form.add_error('rating', 'You must enter rating between 1 and 5')
        else:
            return render(request, 'myapp/review.html', {'form': form})
    else:
        form = ReviewForm()
        return render(request, 'myapp/review.html', {'form': form})


def findcourses(request):
    # breakpoint()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            length = form.cleaned_data['length']
            max_price = form.cleaned_data['max_price']

            if length:
                topics = Topic.objects.filter(length=length)
                course_list = []
                for top in topics:
                    course_list = course_list + list(top.courses.all())
                return render(request, 'myapp/results.html', {'course_list': course_list, 'name': name})
            else:
                course_list = list(Course.objects.filter(price__lte=max_price))
                return render(request, 'myapp/results.html', {'course_list': course_list, 'name': name})
        else:
            return HttpResponse('Invalid data')
    else:
        form = SearchForm()
        return render(request, 'myapp/findcourses.html', {'form': form})


def user_login(request):
    # Create your views here. def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                request.session['last_login'] = ctime()
                # currentTime = timezone.now()
                # request.session['last_login'] = str(currentTime)[:-7]
                request.session.set_expiry(3600)
                return HttpResponseRedirect(reverse('myapp:myaccount'))
            else:
                return HttpResponse('Your last login was more than one hour ago')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse(('myapp:index')))



# @login_required
# def myaccount(request):
#     if (request.user.is_authenticated):
#         count = Student.objects.filter(username__iexact=request.user.username).count()
#         if count == 1:
#             currentUser = Student.objects.get(id=request.user.id)
#             registeredCourses = currentUser.registered_courses.all()
#             interestedTopics = currentUser.interested_in.all()
#             return render(request, 'myapp/myaccount.html', {'first_name': currentUser.first_name,
#                                                             'last_name': currentUser.last_name,
#                                                             'interestedTopics': interestedTopics,
#                                                             'registeredCourses': registeredCourses})
#         else:
#             msg = 'You are not a registered student'
#             return render(request, 'myapp/order_response.html', {'msg': msg})
#
#     else:
#         msg = 'Not Logged In'
#         # return render(request, 'myapp/login.html', {'msg': msg})
#         return HttpResponseRedirect(reverse('myapp:login'))

@login_required
def myaccount(request):
    if (request.user.is_authenticated):
        count = Student.objects.filter(username__iexact=request.user.username).count()
        if count == 1:
            currentUser = Student.objects.get(id=request.user.id)
            registeredCourses = currentUser.registered_courses.all()
            interestedTopics = currentUser.interested_in.all()
            if request.method == 'POST':
                form = ImageUploadForm(request.POST, request.FILES)
                if form.is_valid():
                    currentUser.student_image = form.cleaned_data.get('student_image')
                    currentUser.save()
                    return render(request, 'myapp/myaccount.html', {'first_name': currentUser.first_name,
                                                                    'last_name': currentUser.last_name,
                                                                    'interestedTopics': interestedTopics,
                                                                    'registeredCourses': registeredCourses})
            else:
                form = ImageUploadForm()
                return render(request, 'myapp/myaccount.html', {'first_name': currentUser.first_name,
                                                                'last_name': currentUser.last_name,
                                                                'interestedTopics': interestedTopics,
                                                                'registeredCourses': registeredCourses})
        else:
            msg = 'You are not a registered student'
            return render(request, 'myapp/order_response.html', {'msg': msg})

    else:
        msg = 'Not Logged In'
        # return render(request, 'myapp/login.html', {'msg': msg})
        return HttpResponseRedirect(reverse('myapp:login'))


def register(request):
    msg = ''
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            msg = 'Your data has been registered in our database'
            form.save()
            return render(request, 'myapp/index.html', {'msg': msg})
        else:
            msg = 'Please make sure data entered is correct'
            render(request, 'myapp/register.html', {'msg': msg})
    else:
        form = RegisterForm
    return render(request, 'myapp/register.html', {'form': form, 'msg': msg, })


@login_required
def myorders(request):
    try:
        currentUser = Student.objects.get(id=request.user.id)
    except Student.DoesNotExist:
        currentUser = None

    if currentUser:
        registeredCourses = currentUser.registered_courses.all()
        interestedTopics = currentUser.interested_in.all()
        return render(request, 'myapp/myorders.html', {'first_name': currentUser.first_name,
                                                       'last_name': currentUser.last_name,
                                                       'registeredCourses': registeredCourses})
    else:
        return HttpResponse("You are not a registered student! ")

def forgot_password(request):
    if request.method == "POST":
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                student = Student.objects.get(email=email)
                new_pwd = student.username + "1234"
                student.set_password(new_pwd)
                student.save()
                send_from = 'monkstood1903@gmail.com'
                sent_to = student.email
                mail_content = "Your new password is: " + new_pwd
                send_mail('New Password', mail_content, send_from, [sent_to])

                message = "New password sent to your email id: " + sent_to
                return render(request, 'myapp/forgot_password.html', {'form': form,
                                                                      'message': message})
            except Student.DoesNotExist:
                form= ForgotPasswordForm()
                message = 'Invalid Username, Try Again.'
                return render(request, 'myapp/forgot_password.html', {'form': form,
                                                                      'message': message})
    else:
        form = ForgotPasswordForm()
        return render(request, 'myapp/forgot_password.html', {'form': form})