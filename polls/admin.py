"""This module is for admin interface."""

from django.contrib import admin
from .models import Question, Choice


class ChoiceInline(admin.StackedInline):
    """Tell the admin that Choice objects have an admin interface."""

    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    """Tell the admin that Question objects have an admin interface."""

    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information',
         {'fields': ['pub_date', 'end_date'],
          'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)

# Register your models here.
