from django.urls import path
from django.conf.urls.static import static
from parking import settings
from .views import (
    CreateCustomUserApiView,
    ListCustomUsersApiView,
    ManageUserView,
    ParkingCreateListApiView,
    ParkingUpdateDeleteView,
    TicketCreateListApiView,
    TicketUpdateDeleteView,
    VehicleCreateListApiView,
    VehicleUpdateDeleteView,
    ParkingSectionCreateListApiView,
    ParkingSectionUpdateDeleteView,
    ParkingSlotCreateListApiView,
    ParkingSlotUpdateDeleteView,
    ParkingPriceCreateListApiView,
    ParkingPriceUpdateDeleteView,
    PassesCreateListApiView,
    PassesUpdateDeleteView,
)
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("signup", CreateCustomUserApiView.as_view(), name="signup"),
    path("signin", obtain_auth_token, name="signin"),
    path("me/", ManageUserView.as_view(), name="me"),
    path("users", ListCustomUsersApiView.as_view(), name="users"),
    path("parking", ParkingCreateListApiView.as_view(), name="parking-create-list"),
    path("parking/<int:pk>", ParkingUpdateDeleteView.as_view(), name="parking-crud"),
    path(
        "parking-section",
        ParkingSectionCreateListApiView.as_view(),
        name="parking-section-create-list",
    ),
    path(
        "parking-section/<uuid:pk>",
        ParkingSectionUpdateDeleteView.as_view(),
        name="parking-section-crud",
    ),
    path(
        "parking-slot",
        ParkingSlotCreateListApiView.as_view(),
        name="parking-slot-create-list",
    ),
    path(
        "parking-slot/<uuid:pk>",
        ParkingSlotUpdateDeleteView.as_view(),
        name="parking-slot-crud",
    ),
    path(
        "parking-price",
        ParkingPriceCreateListApiView.as_view(),
        name="parking-price-create-list",
    ),
    path(
        "parking-price/<uuid:pk>",
        ParkingPriceUpdateDeleteView.as_view(),
        name="parking-price-crud",
    ),
    path("passes", PassesCreateListApiView.as_view(), name="passes-create-list"),
    path("passes/<uuid:pk>", PassesUpdateDeleteView.as_view(), name="passes-crud"),
    path("ticket", TicketCreateListApiView.as_view(), name="ticket-create-list"),
    path("ticket/<int:pk>", TicketUpdateDeleteView.as_view(), name="ticket-crud"),
    path("vehicle", VehicleCreateListApiView.as_view(), name="vehicle-create-list"),
    path("vehicle/<int:pk>", VehicleUpdateDeleteView.as_view(), name="vehicle-crud"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
