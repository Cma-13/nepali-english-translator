from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import api

urlpatterns = [
    path("token/", obtain_auth_token, name="api_token"),
    path("translate/", api.TranslateAPIView.as_view(), name="api_translate"),
    path("history/", api.HistoryListAPIView.as_view(), name="api_history"),
    path("history/<int:pk>/", api.HistoryDetailAPIView.as_view(), name="api_history_detail"),
]
