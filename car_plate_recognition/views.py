# recognition/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import CarPlate
from .serializers import CarPlateSerializer
from .plate_recognition import recognize_plate


class CarPlateViewSet(viewsets.ModelViewSet):
    queryset = CarPlate.objects.all()
    serializer_class = CarPlateSerializer
    parser_classes = [MultiPartParser, FormParser]  # для поддержки загрузки файлов

    def create(self, request, *args, **kwargs):
        # Создаем запись и распознаем текст после сохранения изображения
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        car_plate = serializer.save()

        # Обработка изображения и распознавание текста
        car_plate.recognized_text = recognize_plate(car_plate.image.path)
        car_plate.save()

        # Возвращаем ответ с данными новой записи
        headers = self.get_success_headers(serializer.data)
        return Response(self.get_serializer(car_plate).data, status=status.HTTP_201_CREATED, headers=headers)
