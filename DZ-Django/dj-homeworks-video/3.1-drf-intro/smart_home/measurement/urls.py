from django.urls import path
from measurement.views import create_sensor, patch_sensor, create_measurement, show_sensors, SensorView, MeasurementCreaterView

urlpatterns = [
    path('create_sensor/<str:name>/', create_sensor),
    path('patch_sensor/<str:name>/', patch_sensor),
    # path('create_measurement/<int:sensor>/<temperature>/', create_measurement),
    path('create_measurement/', MeasurementCreaterView.as_view()),
    path('show_sensors/', show_sensors),
    path('sensor/<pk>/', SensorView.as_view())
    # TODO: зарегистрируйте необходимые маршруты
]
