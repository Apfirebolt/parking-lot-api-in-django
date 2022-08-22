from django.urls import path
from django.conf.urls.static import static
from parking import settings
from . views import (  CreateCustomUserApiView, ListCustomUsersApiView )
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('signup', CreateCustomUserApiView.as_view(), name='signup'),
    path('signin', obtain_auth_token, name='signin'),
    path('users', ListCustomUsersApiView.as_view(), name='users'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
