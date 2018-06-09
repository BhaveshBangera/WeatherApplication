from django.urls import path
from . import views

app_name = 'weatherapp'

urlpatterns = [
    path('', views.index, name="index"),
    path('<name>', views.details, name="details")
]
