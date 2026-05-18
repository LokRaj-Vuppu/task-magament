from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("task/", include("core.urls")),
    path("account/", include("accounts.urls")),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
