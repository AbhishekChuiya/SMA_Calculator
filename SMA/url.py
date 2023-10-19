from django.urls import path
from .views import SMACalculator

urlpatterns = [
    path('sma/', SMACalculator.as_view(), name='upload-csv'),
]
