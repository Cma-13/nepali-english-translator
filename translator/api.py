from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from .models import Translation
from .preeti import preeti_to_unicode
from .serializers import (
    PreetiRequestSerializer,
    TranslateRequestSerializer,
    TranslationSerializer,
)
from .services import TranslationError, translate_text


class TranslateAPIView(APIView):
    """POST text, get the translation back. The result is saved to history."""

    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "translate"

    def post(self, request):
        serializer = TranslateRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        text = preeti_to_unicode(data["text"]) if data["is_preeti"] else data["text"]

        try:
            result = translate_text(text, data["direction"], data["tone"])
        except TranslationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        translation = Translation.objects.create(
            user=request.user,
            source_text=text,
            translated_text=result,
            direction=data["direction"],
            tone=data["tone"],
        )
        return Response(TranslationSerializer(translation).data, status=status.HTTP_201_CREATED)


class PreetiConvertAPIView(APIView):
    """POST Preeti-typed text, get Nepali Unicode back. Nothing is saved."""

    def post(self, request):
        serializer = PreetiRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"unicode_text": preeti_to_unicode(serializer.validated_data["text"])})


class HistoryListAPIView(generics.ListAPIView):
    """The logged-in user's translations, newest first, 10 per page."""

    serializer_class = TranslationSerializer

    def get_queryset(self):
        return Translation.objects.filter(user=self.request.user)


class HistoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """GET one translation, PATCH its translated_text, or DELETE it.

    Users can only reach their own.
    """

    serializer_class = TranslationSerializer

    def get_queryset(self):
        return Translation.objects.filter(user=self.request.user)
