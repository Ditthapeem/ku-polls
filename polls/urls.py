"""This module contain url patterns are *relative* to 'polls' app."""
from django.urls import path
from . import views

# these url patterns are *relative* to 'polls' app,
# so do not write the 'polls/' at beginning for the path

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote')
]
