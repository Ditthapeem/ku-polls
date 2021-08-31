from django.urls import path
from . import views

# these url patterns are *relative* to 'polls' app,
# so do not write the 'polls/' at beginning for the path

urlpatterns = [
    path('', views.index, name='index')
]
