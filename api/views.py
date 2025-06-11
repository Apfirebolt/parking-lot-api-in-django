from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from . permissions import IsAdmin
from rest_framework import status
from rest_framework.response import Response
from . serializers import CustomUserSerializer, AreaSerializer, TicketSerializer, ParkingSerializer, VehicleSerializer
from . models import CustomUser, Parking, Area, Ticket, Vehicle


class CreateCustomUserApiView(CreateAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()


class ListCustomUsersApiView(ListAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()

class ManageUserView(RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = CustomUserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authentication user"""
        return self.request.user


class AreaCreateListApiView(ListCreateAPIView):
    serializer_class = AreaSerializer
    queryset = Area.objects.all()
    permission_classes = [IsAuthenticated, IsAdmin]

    def perform_create(self, serializer):
        return super().perform_create(serializer)


class AreaUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    serializer_class = AreaSerializer
    queryset = Area.objects.all()
    permission_classes = [IsAuthenticated, IsAdmin]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'message': 'Area successfully deleted',
        }, status=status.HTTP_204_NO_CONTENT)


    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

class ParkingCreateListApiView(ListCreateAPIView):
    serializer_class = ParkingSerializer
    queryset = Parking.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        capacity = self.request.data['capacity']
        if not capacity:
            return Response({
            'message': 'Capacity is required',
        }, status=status.HTTP_400_BAD_REQUEST)

        # Search for first area with given available capacity
        vacant_area = Area.objects.filter(capacity__gte=capacity).first()
        if not vacant_area:
            return Response({
            'message': 'Parking area not available',
        }, status=status.HTTP_403_FORBIDDEN)

        # vacant area is available now create parking slot
        serializer.save(area=vacant_area, user=self.request.user, status='Occupied')

        vacant_area.capacity -= capacity
        vacant_area.save()
        

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            'message': 'Parking lot created',
        }, status=status.HTTP_201_CREATED)
    


class ParkingUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    serializer_class = ParkingSerializer
    queryset = Parking.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'message': 'Parking successfully deleted',
        }, status=status.HTTP_204_NO_CONTENT)


    def update(self,request,*args,**kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance,data = request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'message': 'Parking updated successfully',
            'data': serializer.data
        })

class TicketCreateListApiView(ListCreateAPIView):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            'message': 'Parking Ticket created',
        }, status=status.HTTP_201_CREATED)


class TicketUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    serializer_class = TicketSerializer
    queryset = Parking.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'message': 'Parking Ticket successfully deleted',
        }, status=status.HTTP_204_NO_CONTENT)


    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    

class VehicleCreateListApiView(ListCreateAPIView):
    serializer_class = VehicleSerializer
    queryset = Vehicle.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            'message': 'Vehicle created',
        }, status=status.HTTP_201_CREATED)
    

class VehicleUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    serializer_class = VehicleSerializer
    queryset = Vehicle.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'message': 'Vehicle successfully deleted',
        }, status=status.HTTP_204_NO_CONTENT)


    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    
    
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)