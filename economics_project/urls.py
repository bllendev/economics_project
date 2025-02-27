from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

urlpatterns = [
    # Dango Admin
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    path("admin/", admin.site.urls),
    # User Authentication
    path("accounts/", include("allauth.urls")),
    # User Profiles
    path("", include("users.urls")),
    path("users/", include("users.urls")),
    # Local apps
    path("ai/", include("ai.urls")),
    path("dashboard/", include("dashboard.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
