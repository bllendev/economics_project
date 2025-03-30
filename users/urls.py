from django.urls import path
from users import views


app_name = "users"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    # path("profile", views.ProfileView.as_view(), name="profile"),
    # other paths
]
