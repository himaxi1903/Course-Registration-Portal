from django.contrib import admin

from django.contrib import admin


from .models import Topic, Course, Student, Order, Review


class CourseAdmin(admin.ModelAdmin):
    fields = [('title', 'topic'), ('price', 'num_reviews','for_everyone')]
    actions = ['reduce_by_10']

    def reduce_by_10(self, request, queryset):
        for e in queryset:
            temp = int(e.price) - 0.1 * int(e.price)
            e.price = temp
            e.save()

    list_display = ('title', 'topic', 'price')

class OrderAdmin(admin.ModelAdmin):
    fields = ['courses', ('Student', 'order_status', 'order_date')]
    list_display = ('id', 'Student', 'order_status', 'order_date', 'total_items')


class CourseInline(admin.TabularInline):
    model = Course


class TopicAdmin(admin.ModelAdmin):
    fields = [('name', 'length')]
    list_display = ('name', 'length')
    inlines = [
        CourseInline
    ]

class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'level', 'list_of_registered_courses')

    def list_of_registered_courses(self, obj):
        courses = obj.registered_courses.all()
        list_courses = [c.title for c in courses]
        return list_courses

# Register your models here.
admin.site.register(Topic, TopicAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Review)
