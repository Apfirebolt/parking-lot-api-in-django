import logging
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .permissions import IsAdmin
from rest_framework import status
from rest_framework.response import Response
from .serializers import (
    CustomUserSerializer,
    TicketSerializer,
    ParkingSerializer,
    VehicleSerializer,
    ParkingSectionSerializer,
    PassesSerializer
)
from .models import (
    CustomUser,
    Parking,
    Ticket,
    Vehicle,
    ParkingPrice,
    ParkingSlot,
    ParkingSection,
    Passes
)

# Get an instance of a logger
api_errors_logger = logging.getLogger('api_errors')
parking_logger = logging.getLogger(__name__) # General logger for this module


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


class ParkingCreateListApiView(ListCreateAPIView):
    serializer_class = ParkingSerializer
    queryset = Parking.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        capacity = self.request.data.get("capacity")
        if capacity is None:
            parking_logger.warning(f"Capacity is missing for user: {self.request.user.id}")
            raise ValueError("Capacity is required")

        try:
            serializer.save(user=self.request.user)
            parking_logger.info(f"Parking lot created successfully by user: {self.request.user.id} with capacity: {capacity}")
        except Exception as e:
            parking_logger.error(f"Error saving parking lot for user {self.request.user.id}: {str(e)}")
            raise

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(
                {
                    "message": "Parking lot created",
                },
                status=status.HTTP_201_CREATED,
            )
        except ValueError as ve:
            parking_logger.warning(f"Validation error during parking lot creation: {str(ve)}")
            return Response(
                {
                    "message": str(ve),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            api_errors_logger.exception(f"Unhandled error in ParkingCreateListApiView.create for user {request.user.id}:")
            # `logger.exception()` is a convenient way to log an error with traceback
            return Response(
                {
                    "message": "An error occurred while creating the parking lot.",
                    "error": "Please try again later or contact support.", # Don't expose raw exception to client
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )



class ParkingUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    serializer_class = ParkingSerializer
    queryset = Parking.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {
                "message": "Parking successfully deleted",
            },
            status=status.HTTP_204_NO_CONTENT,
        )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            {"message": "Parking updated successfully", "data": serializer.data}
        )


class ParkingSectionCreateListApiView(ListCreateAPIView):
    serializer_class = ParkingSectionSerializer
    queryset = ParkingSection.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {
                "message": "Parking Section created",
            },
            status=status.HTTP_201_CREATED,
        )


class ParkingSectionUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    serializer_class = ParkingSectionSerializer
    queryset = Parking.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {
                "message": "Parking Section successfully deleted",
            },
            status=status.HTTP_204_NO_CONTENT,
        )

    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


class ParkingSlotCreateListApiView(ListCreateAPIView):
    serializer_class = ParkingSectionSerializer
    queryset = ParkingSlot.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {
                "message": "Parking Slot created",
            },
            status=status.HTTP_201_CREATED,
        )


class ParkingSlotUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    serializer_class = ParkingSectionSerializer
    queryset = ParkingSlot.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {
                "message": "Parking Slot successfully deleted",
            },
            status=status.HTTP_204_NO_CONTENT,
        )

    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


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
        return Response(
            {
                "message": "Parking Ticket created",
            },
            status=status.HTTP_201_CREATED,
        )


class TicketUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    serializer_class = TicketSerializer
    queryset = Parking.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {
                "message": "Parking Ticket successfully deleted",
            },
            status=status.HTTP_204_NO_CONTENT,
        )

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
        return Response(
            {
                "message": "Vehicle created",
            },
            status=status.HTTP_201_CREATED,
        )


class VehicleUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    serializer_class = VehicleSerializer
    queryset = Vehicle.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {
                "message": "Vehicle successfully deleted",
            },
            status=status.HTTP_204_NO_CONTENT,
        )

    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    

class ParkingPriceCreateListApiView(ListCreateAPIView):
    serializer_class = ParkingSectionSerializer
    queryset = ParkingPrice.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {
                "message": "Parking Price created",
            },
            status=status.HTTP_201_CREATED,
        )
    

class ParkingPriceUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    serializer_class = ParkingSectionSerializer
    queryset = ParkingPrice.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {
                "message": "Parking Price successfully deleted",
            },
            status=status.HTTP_204_NO_CONTENT,
        )

    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    

class PassesCreateListApiView(ListCreateAPIView):
    serializer_class = PassesSerializer
    queryset = Passes.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {
                "message": "Passes created",
            },
            status=status.HTTP_201_CREATED,
        )
    
    
class PassesUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    serializer_class = PassesSerializer
    queryset = Passes.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {
                "message": "Passes successfully deleted",
            },
            status=status.HTTP_204_NO_CONTENT,
        )

    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
