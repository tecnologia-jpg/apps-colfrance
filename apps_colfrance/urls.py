from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("app_silos/", include("aforo_silos.urls")),
    path("app_control/", include("control_plagas.urls")),
    path("app_rh/", include("recursos_humanos.urls")),
    path("", include("web_colfrance.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
