from django.urls import path

from . import views

urlpatterns = [
    path("", views.translate, name="home"),
    path("history/", views.history, name="history"),
    path("history/<int:pk>/", views.history_detail, name="history_detail"),
    path("history/<int:pk>/delete/", views.history_delete, name="history_delete"),
]
