from django.urls import path
from django.conf.urls.static import static
from parking import settings
from . views import (  CreateCustomUserApiView, ListCustomUsersApiView, AreaCreateListApiView, AreaUpdateDeleteView, \
    ParkingCreateListApiView, ParkingUpdateDeleteView, TicketCreateListApiView, TicketUpdateDeleteView )
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('signup', CreateCustomUserApiView.as_view(), name='signup'),
    path('signin', obtain_auth_token, name='signin'),
    path('users', ListCustomUsersApiView.as_view(), name='users'),
    path('area', AreaCreateListApiView.as_view(), name='area-create-list'),
    path('area/<int:pk>', AreaUpdateDeleteView.as_view(), name='area-crud'),
    path('parking', ParkingCreateListApiView.as_view(), name='parking-create-list'),
    path('parking/<int:pk>', ParkingUpdateDeleteView.as_view(), name='parking-crud'),
    path('ticket', TicketCreateListApiView.as_view(), name='ticket-create-list'),
    path('ticket/<int:pk>', TicketUpdateDeleteView.as_view(), name='ticket-crud'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
