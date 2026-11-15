from django.urls import path

from . import views

urlpatterns = [
    path("", views.translate, name="home"),
    path("preeti/", views.preeti_converter, name="preeti"),
    path("history/", views.history, name="history"),
    path("history/<int:pk>/", views.history_detail, name="history_detail"),
    path("history/<int:pk>/delete/", views.history_delete, name="history_delete"),
    path("history/<int:pk>/download/", views.history_download, name="history_download"),
]
