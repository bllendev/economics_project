from django.urls import path
from users import views


urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    # other paths
]
