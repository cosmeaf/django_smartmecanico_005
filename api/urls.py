from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView


# Applications Routes
from smartmecanico.views.address_view import AddressModelViewSet
from smartmecanico.views.vehicle_view import VehicleModelViewSet
from smartmecanico.views.user_view import CustomUserModelViewSet
from smartmecanico.views.services_view import ServiceModelViewSet, HourServiceModelViewSet
from employee_management.views import EmployeeInfoModelViewSet
from smartmecanico.views.appointment_view import AppointmentModelViewSet


# Default Route Django Rest Framework
router = DefaultRouter()
router.register(r'users', CustomUserModelViewSet, basename='users')
router.register(r'addresses', AddressModelViewSet, basename='addresses')
router.register(r'vehicles', VehicleModelViewSet, basename='vehicles')
router.register(r'service', ServiceModelViewSet, basename='service')
router.register(r'hourservice', HourServiceModelViewSet, basename='hourservice')
router.register(r'employee', EmployeeInfoModelViewSet, basename='employee')
router.register(r'appointment', AppointmentModelViewSet, basename='appointment')

# Site Custom
admin.site.index_title = settings.INDEX_TITLE
admin.site.site_header = settings.ADMIN_SITE_HEADER
admin.site.site_title = settings.ADMIN_SITE_TITLE


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/', include((router.urls))),
    re_path(r'api/', include(router.urls)),
    path('api/', include('security.urls')),    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)