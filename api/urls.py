from django.urls import path
from django.conf.urls.static import static
from parking import settings
from . views import (  CreateCustomUserApiView, ListCustomUsersApiView, AreaCreateListApiView, AreaUpdateDeleteView )
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('signup', CreateCustomUserApiView.as_view(), name='signup'),
    path('signin', obtain_auth_token, name='signin'),
    path('users', ListCustomUsersApiView.as_view(), name='users'),
    path('area', AreaCreateListApiView.as_view(), name='area-create-list'),
    path('area/<int:pk>', AreaUpdateDeleteView.as_view(), name='area-crud'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
