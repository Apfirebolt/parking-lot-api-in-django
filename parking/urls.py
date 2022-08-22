from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from parking import settings
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='home_page.html'), name='home'),
    path('admin/', admin.site.urls),
    path('api/', include(('api.urls', 'api'), namespace='api')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
