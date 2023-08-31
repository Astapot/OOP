from django.urls import path
from measurement.views import create_sensor, patch_sensor, create_measurement

urlpatterns = [
    path('create_sensor/<str:name>/', create_sensor),
    path('patch_sensor/<str:name>/', patch_sensor),
    path('create_measurement/<int:sensor_id>/<temperature>/', create_measurement)
    # TODO: зарегистрируйте необходимые маршруты
]
