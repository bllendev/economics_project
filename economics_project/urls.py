from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

urlpatterns = [
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("", include("users.urls", namespace="users")),
    path("ai/", include("ai.urls", namespace="ai")),
    path("dashboard/", include("dashboard.urls", namespace="dashboard")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
