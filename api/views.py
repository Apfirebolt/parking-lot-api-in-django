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
    PassesSerializer,
    ParkingSlotSerializer,
    ParkingPriceSerializer
)
from .models import (
    CustomUser,
    Parking,
    Ticket,
    Vehicle,
    ParkingPrice,
    ParkingSlot,
    ParkingSection,
    Passes,
)

# Get an instance of a logger
api_errors_logger = logging.getLogger("api_errors")
parking_logger = logging.getLogger(__name__)  # General logger for this module


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
            parking_logger.warning(
                f"Capacity is missing for user: {self.request.user.id}"
            )
            raise ValueError("Capacity is required")

        try:
            serializer.save(user=self.request.user)
            parking_logger.info(
                f"Parking lot created successfully by user: {self.request.user.id} with capacity: {capacity}"
            )
        except Exception as e:
            parking_logger.error(
                f"Error saving parking lot for user {self.request.user.id}: {str(e)}"
            )
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
            parking_logger.warning(
                f"Validation error during parking lot creation: {str(ve)}"
            )
            return Response(
                {
                    "message": str(ve),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            api_errors_logger.exception(
                f"Unhandled error in ParkingCreateListApiView.create for user {request.user.id}:"
            )
            # `logger.exception()` is a convenient way to log an error with traceback
            return Response(
                {
                    "message": "An error occurred while creating the parking lot.",
                    "error": "Please try again later or contact support.",  # Don't expose raw exception to client
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ParkingUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    serializer_class = ParkingSerializer
    queryset = Parking.objects.all()

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            parking_logger.info(
                f"Parking with id {instance.id} deleted by user {request.user.id}"
            )
            return Response(
                {
                    "message": "Parking successfully deleted",
                },
                status=status.HTTP_204_NO_CONTENT,
            )
        except Exception as e:
            api_errors_logger.exception(
                f"Error deleting parking with id {getattr(instance, 'id', None)} by user {request.user.id}: {str(e)}"
            )
            return Response(
                {
                    "message": "An error occurred while deleting the parking.",
                    "error": "Please try again later or contact support.",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            parking_logger.info(
                f"Parking with id {instance.id} updated by user {request.user.id}"
            )
            return Response(
                {"message": "Parking updated successfully", "data": serializer.data}
            )
        except Exception as e:
            api_errors_logger.exception(
                f"Error updating parking with id {getattr(instance, 'id', None)} by user {request.user.id}: {str(e)}"
            )
            return Response(
                {
                    "message": "An error occurred while updating the parking.",
                    "error": "Please try again later or contact support.",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ParkingSectionCreateListApiView(ListCreateAPIView):
    serializer_class = ParkingSectionSerializer
    queryset = ParkingSection.objects.all()
    permission_classes = [IsAuthenticated]

    # perform_create method is removed and its logic is moved here
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # --- DEBUGGING LOG: Log validated_data right before save ---
            api_errors_logger.debug(f"DEBUG: validated_data before serializer.save(): {serializer.validated_data}")
        
            serializer.save()
            parking_logger.info("Parking Section created")

            return Response(
                {
                    "message": "Parking Section created",
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            api_errors_logger.exception("Unhandled error in ParkingSectionCreateListApiView.create for user %s", self.request.user.id)
            return Response(
                {
                    "message": "New errors to come.",
                    "error": "Please try again later or contact support.",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ParkingSectionUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    serializer_class = ParkingSectionSerializer
    queryset = ParkingSection.objects.all()

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            parking_logger.info(
                f"Parking Section with id {instance.id} deleted"
            )
            return Response(
                {
                    "message": "Parking Section successfully deleted",
                },
                status=status.HTTP_204_NO_CONTENT,
            )
        except Exception as e:
            api_errors_logger.exception(
                f"Error deleting Parking Section with id {getattr(instance, 'id', None)} by user {request.user.id}: {str(e)}"
            )
            return Response(
                {
                    "message": "An error occurred while deleting the Parking Section.",
                    "error": "Please try again later or contact support.",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ParkingSlotCreateListApiView(ListCreateAPIView):
    serializer_class = ParkingSlotSerializer
    queryset = ParkingSlot.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        try:
            serializer.save()
            parking_logger.info("Parking Slot created")
        except Exception as e:
            api_errors_logger.exception("Error creating Parking Slot by user")
            raise

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(
                {
                    "message": "Parking Slot created",
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            api_errors_logger.exception(
                f"Unhandled error in ParkingSlotCreateListApiView.create for user {request.user.id}: {str(e)}"
            )
            return Response(
                {
                    "message": "An error occurred while creating the Parking Slot.",
                    "error": "Please try again later or contact support.",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ParkingSlotUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    serializer_class = ParkingSlotSerializer
    queryset = ParkingSlot.objects.all()

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            parking_logger.info(
                f"Parking Slot with id {instance.id} deleted by user {request.user.id}"
            )
            return Response(
                {
                    "message": "Parking Slot successfully deleted",
                },
                status=status.HTTP_204_NO_CONTENT,
            )
        except Exception as e:
            api_errors_logger.exception(
                f"Error deleting Parking Slot with id {getattr(instance, 'id', None)} by user {request.user.id}: {str(e)}"
            )
            return Response(
                {
                    "message": "An error occurred while deleting the Parking Slot.",
                    "error": "Please try again later or contact support.",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request, *args, **kwargs):
        try:
            response = super().put(request, *args, **kwargs)
            parking_logger.info(
                f"Parking Slot with id {getattr(self.get_object(), 'id', None)} updated by user {request.user.id}"
            )
            return response
        except Exception as e:
            api_errors_logger.exception(
                f"Error updating Parking Slot with id {getattr(self.get_object(), 'id', None)} by user {request.user.id}: {str(e)}"
            )
            return Response(
                {
                    "message": "An error occurred while updating the Parking Slot.",
                    "error": "Please try again later or contact support.",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


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
        try:
            serializer.save(user=self.request.user)
            parking_logger.info(f"Vehicle created by user: {self.request.user.id}")
        except Exception as e:
            api_errors_logger.exception(
                f"Error creating Vehicle by user {self.request.user.id}: {str(e)}"
            )
            raise

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(
                {
                    "message": "Vehicle created",
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            api_errors_logger.exception(
                f"Unhandled error in VehicleCreateListApiView.create for user {request.user.id}: {str(e)}"
            )
            return Response(
                {
                    "message": "An error occurred while creating the Vehicle.",
                    "error": "Please try again later or contact support.",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class VehicleUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    serializer_class = VehicleSerializer
    queryset = Vehicle.objects.all()

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            parking_logger.info(
                f"Vehicle with id {instance.id} deleted by user {request.user.id}"
            )
            return Response(
                {
                    "message": "Vehicle successfully deleted",
                },
                status=status.HTTP_204_NO_CONTENT,
            )
        except Exception as e:
            api_errors_logger.exception(
                f"Error deleting Vehicle with id {getattr(instance, 'id', None)} by user {request.user.id}: {str(e)}"
            )
            return Response(
                {
                    "message": "An error occurred while deleting the Vehicle.",
                    "error": "Please try again later or contact support.",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request, *args, **kwargs):
        try:
            response = super().put(request, *args, **kwargs)
            parking_logger.info(
                f"Vehicle with id {getattr(self.get_object(), 'id', None)} updated by user {request.user.id}"
            )
            return response
        except Exception as e:
            api_errors_logger.exception(
                f"Error updating Vehicle with id {getattr(self.get_object(), 'id', None)} by user {request.user.id}: {str(e)}"
            )
            return Response(
                {
                    "message": "An error occurred while updating the Vehicle.",
                    "error": "Please try again later or contact support.",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ParkingPriceCreateListApiView(ListCreateAPIView):
    serializer_class = ParkingPriceSerializer
    queryset = ParkingPrice.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        try:
            serializer.save()
            parking_logger.info(
                f"Parking Price created by user: {self.request.user.id}"
            )
        except Exception as e:
            api_errors_logger.exception(
                f"Error creating Parking Price by user {self.request.user.id}: {str(e)}"
            )
            raise

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(
                {
                    "message": "Parking Price created",
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            api_errors_logger.exception(
                f"Unhandled error in ParkingPriceCreateListApiView.create for user {request.user.id}: {str(e)}"
            )
            return Response(
                {
                    "message": "An error occurred while creating the Parking Price.",
                    "error": "Please try again later or contact support.",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ParkingPriceUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    serializer_class = ParkingPriceSerializer
    queryset = ParkingPrice.objects.all()

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            parking_logger.info(
                f"Parking Price with id {instance.id} deleted by user {request.user.id}"
            )
            return Response(
                {
                    "message": "Parking Price successfully deleted",
                },
                status=status.HTTP_204_NO_CONTENT,
            )
        except Exception as e:
            api_errors_logger.exception(
                f"Error deleting Parking Price with id {getattr(instance, 'id', None)} by user {request.user.id}: {str(e)}"
            )
            return Response(
                {
                    "message": "An error occurred while deleting the Parking Price.",
                    "error": "Please try again later or contact support.",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request, *args, **kwargs):
        try:
            response = super().put(request, *args, **kwargs)
            parking_logger.info(
                f"Parking Price with id {getattr(self.get_object(), 'id', None)} updated by user {request.user.id}"
            )
            return response
        except Exception as e:
            api_errors_logger.exception(
                f"Error updating Parking Price with id {getattr(self.get_object(), 'id', None)} by user {request.user.id}: {str(e)}"
            )
            return Response(
                {
                    "message": "An error occurred while updating the Parking Price.",
                    "error": "Please try again later or contact support.",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class PassesCreateListApiView(ListCreateAPIView):
    serializer_class = PassesSerializer
    queryset = Passes.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
            parking_logger.info(f"Passes created by user: {self.request.user.id}")
        except Exception as e:
            api_errors_logger.exception(
                f"Error creating Passes by user {self.request.user.id}: {str(e)}"
            )
            raise

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(
                {
                    "message": "Passes created",
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            api_errors_logger.exception(
                f"Unhandled error in PassesCreateListApiView.create for user {request.user.id}: {str(e)}"
            )
            return Response(
                {
                    "message": "An error occurred while creating the Passes.",
                    "error": "Please try again later or contact support.",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class PassesUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    serializer_class = PassesSerializer
    queryset = Passes.objects.all()

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            parking_logger.info(
                f"Passes with id {instance.id} deleted by user {request.user.id}"
            )
            return Response(
                {
                    "message": "Passes successfully deleted",
                },
                status=status.HTTP_204_NO_CONTENT,
            )
        except Exception as e:
            api_errors_logger.exception(
                f"Error deleting Passes with id {getattr(instance, 'id', None)} by user {request.user.id}: {str(e)}"
            )
            return Response(
                {
                    "message": "An error occurred while deleting the Passes.",
                    "error": "Please try again later or contact support.",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request, *args, **kwargs):
        try:
            response = super().put(request, *args, **kwargs)
            parking_logger.info(
                f"Passes with id {getattr(self.get_object(), 'id', None)} updated by user {request.user.id}"
            )
            return response
        except Exception as e:
            api_errors_logger.exception(
                f"Error updating Passes with id {getattr(self.get_object(), 'id', None)} by user {request.user.id}: {str(e)}"
            )
            return Response(
                {
                    "message": "An error occurred while updating the Passes.",
                    "error": "Please try again later or contact support.",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
