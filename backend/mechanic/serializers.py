from rest_framework import serializers
from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [
            "id",
            "sender",
            "message",
            "media_url",
            "media_type",
            "created_at",
        ]


class ChatSerializer(serializers.Serializer):
    session_id = serializers.CharField(max_length=100)
    message = serializers.CharField()


class UploadSerializer(serializers.Serializer):
    session_id = serializers.CharField(max_length=100)
    file = serializers.FileField()


class DiagnosisSerializer(serializers.Serializer):
    session_id = serializers.CharField(max_length=100)


class BookingSerializer(serializers.Serializer):
    session_id = serializers.CharField(max_length=100)
    customer_name = serializers.CharField(max_length=100)
    phone = serializers.CharField(max_length=20)
    car_model = serializers.CharField(max_length=100)
    preferred_date = serializers.DateField()
    preferred_time = serializers.TimeField()
    service = serializers.CharField(max_length=255)