from django.conf.urls.static import static
from django.urls import path

from django_app import settings

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add", views.add, name="add"),
    path("update/<int:task_id>/", views.update, name="update"),
    path("delete/<int:task_id>/", views.delete, name="delete"),
    path("delete_all/", views.delete_all, name="delete_all"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
