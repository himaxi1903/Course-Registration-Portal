# Create your models here.
from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

class Topic(models.Model):
    name = models.CharField(max_length=200)
    length = models.IntegerField(default=12)
    def __str__(self):
        return '{}/{}'.format(self.name, self.length)

def validate_price(value):
        if value < 50 or value > 500:
            raise ValidationError(
                ('%(value)s should be between $50 and $500'), params={'value': value},
            )


class Course(models.Model):
    title = models.CharField(max_length=200)
    topic = models.ForeignKey(Topic, related_name='courses',
                              on_delete=models.CASCADE)
    price = models.DecimalField(validators=[validate_price],max_digits=10, decimal_places=2)
    for_everyone = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    num_reviews = models.PositiveIntegerField(default=0)
    def __str__(self):
        return '{}/{}'.format(self.title, self.topic, self.price, self.for_everyone, self.description)



class Student(User):
    LVL_CHOICES = [
        ('HS', 'High School'),
        ('UG', 'Undergraduate'),
        ('PG', 'Postgraduate'),
        ('ND', 'No Degree'),
    ]
    level = models.CharField(choices=LVL_CHOICES, max_length=2, default='HS')
    address = models.CharField(max_length=300, default=True)
    # email = models.CharField(max_length=100)
    province = models.CharField(max_length=2, default='ON')
    registered_courses = models.ManyToManyField(Course, blank=True)
    interested_in = models.ManyToManyField(Topic)
    student_image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return '{}/{}'.format(self.first_name, self.last_name, self.registered_courses)


class Order(models.Model):
    VL_CHOICES = [
        (0, 'Cancelled'),
        (1, 'Confirmed'),
        (2, 'On hold'),
    ]
    courses = models.ManyToManyField(Course)
    Student = models.ForeignKey(Student, on_delete=models.CASCADE)
    order_status = models.IntegerField(choices=VL_CHOICES, default=1)
    order_date = models.DateField(default=datetime.date.today)
    def __str__(self):
        return '{}/{}'.format(self.courses, self.Student, self.order_status, self.order_date)
    def total_cost(self):
        cost = 0
        for course in self.courses.all():
            cost += course.price
        return cost

    def total_items(self):
        return self.courses.all().count()


class Review(models.Model):
    reviewer = models.EmailField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comments = models.TextField(blank=True)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return '{}/{}'.format(self.course, self.rating, self.comments, self.date)
















