from django.urls import path
from .views import (
    chat,
    upload_media,
    create_diagnosis,
    create_booking,
    get_booking,
)

urlpatterns = [
    path("chat/", chat, name="chat"),
    path("upload/", upload_media, name="upload"),
    path("diagnosis/", create_diagnosis, name="diagnosis"),
    path("booking/", create_booking, name="create_booking"),
    path("booking/<int:booking_id>/", get_booking, name="get_booking"),
]