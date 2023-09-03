# TODO: опишите необходимые обработчики, рекомендуется использовать generics APIView классы:
# TODO: ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView
from rest_framework.decorators import api_view
from .models import Sensor, Measurement
from rest_framework.response import Response
from .serializers import SensorSerializer, MeasurementSerializer, SensorDetailSerializer
from rest_framework.generics import RetrieveAPIView
from rest_framework import generics
@api_view(['GET'])
def show_sensors(request):
    sensors = Sensor.objects.all()
    data = SensorSerializer(sensors, many=True)
    return Response(data.data)


@api_view(['POST'])
def create_sensor(request, name):
    description = request.GET.get('description', 'No description')
    Sensor(name=name, description=description).save()
    return Response({'status': 'sensor was added'})


@api_view(['PATCH'])
def patch_sensor(request, name):
    new_name = request.GET.get('new_name', 'No name')
    description = request.GET.get('description', 'No description')
    sensor = Sensor.objects.filter(name=name).update(name=new_name, description=description)
    return Response({'status': 'sensor was patched'})


@api_view(['POST'])
def create_measurement(request, sensor, temperature):
    measurement = Measurement(sensor=sensor, temperature=temperature).save()
    return Response({'status': 'measurement was added'})


class SensorView(RetrieveAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorDetailSerializer


class MeasurementCreaterView(generics.ListCreateAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
