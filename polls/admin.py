from django.contrib import admin
from .models import Question

# tell the admin that Question objects have an admin interface.

admin.site.register(Question)

# Register your models here.
