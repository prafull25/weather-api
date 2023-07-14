from django.urls import path
from .views import WeatherAPIView

app_name = 'weather'

urlpatterns = [
    path('weather', WeatherAPIView.as_view(), name='weather_api'),
]
