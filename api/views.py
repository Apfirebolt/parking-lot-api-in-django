from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from . serializers import CustomUserSerializer, AreaSerializer
from . models import CustomUser, Parking, Area, Ticket


class CreateCustomUserApiView(CreateAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()


class ListCustomUsersApiView(ListAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()


class AreaCreateListApiView(ListCreateAPIView):
    serializer_class = AreaSerializer
    queryset = Area.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        return super().perform_create(serializer)


class AreaUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    serializer_class = AreaSerializer
    queryset = Area.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'message': 'Area successfully deleted',
        }, status=status.HTTP_204_NO_CONTENT)


    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)