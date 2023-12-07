
from django.contrib import admin
from django.urls import path, include
from main import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    # intègre l'authentification
    path("accounts/", include("django.contrib.auth.urls")),
    # redicrection après la page login
    path('accounts/profile/', views.hello, name="hello"),
]
