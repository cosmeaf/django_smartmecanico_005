from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,TokenVerifyView)
from rest_framework.routers import DefaultRouter

# Applications Routes
from address.views import AddressViewSet
from vehicle.views import VehicleModelViewSet
from services.views import ServiceModelViewSet, HourServiceModelViewSet
from appointment.views import AppointmentModelViewSet
from employee_management.views import EmployeeInfoModelViewSet

# Default Route Django Rest Framework
router = DefaultRouter()
router.register(r'address', AddressViewSet)
router.register(r'vehicle', VehicleModelViewSet)
router.register(r'service', ServiceModelViewSet)
router.register(r'hourservice', HourServiceModelViewSet)
router.register(r'employee', EmployeeInfoModelViewSet)
router.register(r'appointment', AppointmentModelViewSet)


urlpatterns = [
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/', include('security.urls')),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    re_path(r'^api/', include(router.urls)),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)