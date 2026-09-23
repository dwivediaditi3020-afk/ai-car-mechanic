from django.db import models
import uuid


class Conversation(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    session_id = models.CharField(
        max_length=100,
        unique=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.session_id


class Message(models.Model):
    SENDER_CHOICES = [
        ("user", "User"),
        ("bot", "Bot"),
    ]

    MEDIA_CHOICES = [
        ("text", "Text"),
        ("image", "Image"),
        ("audio", "Audio"),
        ("video", "Video"),
    ]

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages"
    )
    sender = models.CharField(
        max_length=10,
        choices=SENDER_CHOICES
    )
    message = models.TextField(
        blank=True
    )

    media_url = models.FileField(
        upload_to="uploads/",
        blank=True,
        null=True
    )

    media_type = models.CharField(
        max_length=10,
        choices=MEDIA_CHOICES,
        default="text"
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.sender} - {self.media_type}"


class Diagnosis(models.Model):
    CONFIDENCE_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]

    conversation = models.OneToOneField(
        Conversation,
        on_delete=models.CASCADE,
        related_name="diagnosis"
    )
    problem = models.TextField()
    diagnosis = models.TextField()
    confidence = models.CharField(
        max_length=10,
        choices=CONFIDENCE_CHOICES
    )
    recommended_service = models.CharField(
        max_length=255
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.diagnosis[:50]


class Booking(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    diagnosis = models.ForeignKey(
        Diagnosis,
        on_delete=models.CASCADE,
        related_name="bookings"
    )
    customer_name = models.CharField(
        max_length=100
    )
    phone = models.CharField(
        max_length=20
    )
    car_model = models.CharField(
        max_length=100
    )
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    service = models.CharField(
        max_length=255
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.customer_name} - {self.car_model}"