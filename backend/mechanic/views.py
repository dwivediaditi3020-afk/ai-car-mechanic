from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Conversation, Message, Diagnosis, Booking
from .serializers import (
    ChatSerializer,
    UploadSerializer,
    DiagnosisSerializer,
    BookingSerializer,
)


# ============================================================
# CHAT
# ============================================================

@api_view(["POST"])
def chat(request):
    serializer = ChatSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    session_id = serializer.validated_data["session_id"]
    user_message = serializer.validated_data["message"].strip()

    if not user_message:
        return Response(
            {
                "success": False,
                "error": "Message cannot be empty.",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    conversation, created = Conversation.objects.get_or_create(
        session_id=session_id
    )

    # Save user message
    Message.objects.create(
        conversation=conversation,
        sender="user",
        message=user_message,
        media_type="text",
    )

    # Generate mechanic response
    bot_response = generate_mechanic_response(
        user_message,
        conversation,
    )

    # Save bot response
    bot_message = Message.objects.create(
        conversation=conversation,
        sender="bot",
        message=bot_response,
        media_type="text",
    )

    return Response(
        {
            "success": True,
            "session_id": session_id,
            "message": bot_response,
            "message_id": bot_message.id,
        },
        status=status.HTTP_200_OK,
    )


# ============================================================
# MECHANIC RESPONSE LOGIC
# ============================================================

def generate_mechanic_response(user_message, conversation):
    user_message_lower = user_message.lower()

    previous_messages = Message.objects.filter(
        conversation=conversation,
        sender="user",
    ).order_by("created_at")

    full_text = " ".join(
        message.message.lower()
        for message in previous_messages
        if message.message
    )

    # --------------------------------------------------------
    # Keywords
    # --------------------------------------------------------

    engine_words = [
        "engine",
        "motor",
        "rattling",
        "knocking",
        "clicking",
        "grinding",
        "engine sound",
        "engine noise",
        "strange noise",
        "weird noise",
        "unusual noise",
        "strange sound",
        "weird sound",
        "unusual sound",
    ]

    noise_types = [
        "rattling",
        "knocking",
        "clicking",
        "grinding",
        "noise",
        "sound",
    ]

    driving_conditions = [
        "startup",
        "start up",
        "starting",
        "acceleration",
        "accelerating",
        "accelerate",
        "idling",
        "idle",
        "driving",
        "while driving",
    ]

    # --------------------------------------------------------
    # Detect engine/noise issue
    # --------------------------------------------------------

    has_engine_issue = any(
        word in full_text
        for word in engine_words
    )

    has_noise_type = any(
        word in full_text
        for word in noise_types
    )

    has_driving_condition = any(
        word in full_text
        for word in driving_conditions
    )

    if has_engine_issue or has_noise_type:

        # We have noise + condition
        if has_noise_type and has_driving_condition:
            return (
                "Based on what you've described, the vehicle "
                "has an unusual mechanical noise that occurs "
                "under a specific driving condition. Possible "
                "causes include a loose component, exhaust or "
                "heat-shield vibration, or another mechanical "
                "issue.\n\n"
                "You can now generate a diagnosis for this issue."
            )

        # We know the type of noise but not when it occurs
        if has_noise_type and not has_driving_condition:
            return (
                "I understand that your car is making an "
                "unusual noise. To narrow down the possible "
                "cause, when does the noise occur — during "
                "startup, acceleration, idling, braking, "
                "turning, or while driving?"
            )

        # We know the condition but not the noise
        if has_driving_condition and not has_noise_type:
            return (
                "When the noise occurs, what does it sound like? "
                "For example, is it rattling, knocking, clicking, "
                "grinding, squealing, or humming?"
            )

        # Engine mentioned but insufficient information
        return (
            "I can help troubleshoot the engine issue. "
            "Please describe the type of noise or symptom "
            "you are experiencing and when it occurs."
        )

    # --------------------------------------------------------
    # Brake issue
    # --------------------------------------------------------

    if "brake" in full_text:
        return (
            "A brake-related problem can have several causes. "
            "Please tell me whether you are experiencing "
            "squeaking, grinding, vibration, reduced braking "
            "performance, or a soft brake pedal."
        )

    # --------------------------------------------------------
    # Battery / starting issue
    # --------------------------------------------------------

    if (
        "battery" in full_text
        or "won't start" in full_text
        or "wont start" in full_text
        or "not starting" in full_text
        or "doesn't start" in full_text
        or "doesnt start" in full_text
    ):
        return (
            "This may be related to the battery or starting "
            "system. When you try to start the car, do you hear "
            "clicking, does the engine crank slowly, or is there "
            "no response at all?"
        )

    # --------------------------------------------------------
    # Overheating
    # --------------------------------------------------------

    if (
        "overheat" in full_text
        or "overheating" in full_text
        or "temperature is high" in full_text
        or "temperature high" in full_text
    ):
        return (
            "An overheating issue can be related to coolant, "
            "the radiator, thermostat, cooling fan, or another "
            "cooling-system component. Please tell me whether "
            "you see a high-temperature warning, steam, or "
            "coolant leakage."
        )

    # --------------------------------------------------------
    # Tyre / Tire issue
    # --------------------------------------------------------

    if (
        "tyre" in full_text
        or "tire" in full_text
    ):
        return (
            "For a tyre-related issue, please tell me whether "
            "you are experiencing low pressure, a puncture, "
            "uneven wear, vibration, or the vehicle pulling "
            "to one side."
        )

    # --------------------------------------------------------
    # Oil issue
    # --------------------------------------------------------

    if "oil" in full_text:
        return (
            "An oil-related issue can involve low oil level, "
            "an oil leak, or an oil-pressure problem. Please "
            "tell me whether you see an oil warning light, "
            "oil leakage, or unusual engine noise."
        )

    # --------------------------------------------------------
    # AC issue
    # --------------------------------------------------------

    if (
        "ac" in full_text
        or "air conditioning" in full_text
        or "air conditioner" in full_text
    ):
        return (
            "For the AC issue, please tell me whether the AC "
            "is not cooling, cooling weakly, making unusual "
            "noise, or producing an unusual smell."
        )

    # --------------------------------------------------------
    # General car-related question
    # --------------------------------------------------------

    car_words = [
        "car",
        "vehicle",
        "dashboard",
        "clutch",
        "gear",
        "steering",
        "headlight",
        "light",
        "fuel",
        "petrol",
        "diesel",
        "coolant",
        "radiator",
    ]

    if any(word in full_text for word in car_words):
        return (
            "I can help troubleshoot your car problem. "
            "Please describe the symptom in detail, including "
            "when it happens and anything unusual you notice."
        )

    # --------------------------------------------------------
    # Off-topic fallback
    # --------------------------------------------------------

    return (
        "I'm your virtual automobile mechanic, so I can help "
        "with car-related problems such as engine issues, "
        "brakes, battery, tyres, overheating, AC, and other "
        "mechanical symptoms. Please describe the car problem "
        "you're experiencing."
    )


# ============================================================
# MEDIA UPLOAD
# ============================================================

@api_view(["POST"])
def upload_media(request):
    serializer = UploadSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    session_id = serializer.validated_data["session_id"]
    uploaded_file = serializer.validated_data["file"]

    # Get existing conversation or create one
    conversation, created = Conversation.objects.get_or_create(
        session_id=session_id
    )

    content_type = (uploaded_file.content_type or "").lower()
    file_name = uploaded_file.name.lower()

    if content_type.startswith("image/") or file_name.endswith(
        (".jpg", ".jpeg", ".png", ".gif", ".webp")
    ):
        media_type = "image"

    elif content_type.startswith("audio/") or file_name.endswith(
        (".mp3", ".wav", ".ogg", ".m4a", ".aac")
    ):
        media_type = "audio"

    elif content_type.startswith("video/") or file_name.endswith(
        (".mp4", ".mov", ".avi", ".mkv", ".webm", ".m4v")
    ):
        media_type = "video"

    else:
        return Response(
            {
                "success": False,
                "error": (
                    "Only image, audio, and video files "
                    "are supported."
                ),
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    message = Message.objects.create(
        conversation=conversation,
        sender="user",
        message="",
        media_url=uploaded_file,
        media_type=media_type,
    )

    return Response(
        {
            "success": True,
            "message_id": message.id,
            "media_type": media_type,
            "file_name": uploaded_file.name,
            "media_url": message.media_url.url,
            "message": "Media uploaded successfully.",
        },
        status=status.HTTP_201_CREATED,
    )

# ============================================================
# CREATE DIAGNOSIS
# ============================================================

@api_view(["POST"])
def create_diagnosis(request):
    serializer = DiagnosisSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    session_id = serializer.validated_data["session_id"]

    try:
        conversation = Conversation.objects.get(
            session_id=session_id
        )
    except Conversation.DoesNotExist:
        return Response(
            {
                "success": False,
                "error": "Conversation not found.",
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    user_messages = Message.objects.filter(
        conversation=conversation,
        sender="user",
    ).order_by("created_at")

    if not user_messages.exists():
        return Response(
            {
                "success": False,
                "error": "No user messages found for diagnosis.",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    conversation_text = " ".join(
        message.message.lower()
        for message in user_messages
        if message.message
    )

    # --------------------------------------------------------
    # Brake diagnosis
    # --------------------------------------------------------

    if "brake" in conversation_text:
        problem = "Brake-related issue"

        diagnosis = (
            "The symptoms suggest a possible brake system issue. "
            "The brake pads, discs, or related components should "
            "be inspected."
        )

        confidence = "medium"

        recommended_service = (
            "Brake inspection and servicing"
        )

    # --------------------------------------------------------
    # Battery / starting diagnosis
    # --------------------------------------------------------

    elif (
        "battery" in conversation_text
        or "start" in conversation_text
    ):
        problem = "Starting or battery-related issue"

        diagnosis = (
            "The symptoms may indicate a weak battery, poor "
            "battery connection, or another starting-system "
            "issue."
        )

        confidence = "medium"

        recommended_service = (
            "Battery and starting-system inspection"
        )

    # --------------------------------------------------------
    # Overheating diagnosis
    # --------------------------------------------------------

    elif (
        "overheat" in conversation_text
        or "overheating" in conversation_text
    ):
        problem = "Engine overheating"

        diagnosis = (
            "The symptoms suggest a possible cooling-system "
            "problem. Coolant level, radiator, thermostat, "
            "and cooling fan should be inspected."
        )

        confidence = "medium"

        recommended_service = (
            "Cooling-system inspection"
        )

    # --------------------------------------------------------
    # Tyre diagnosis
    # --------------------------------------------------------

    elif (
        "tyre" in conversation_text
        or "tire" in conversation_text
    ):
        problem = "Tyre-related issue"

        diagnosis = (
            "The symptoms suggest a possible tyre pressure, "
            "puncture, wear, or wheel-related issue."
        )

        confidence = "medium"

        recommended_service = (
            "Tyre and wheel inspection"
        )

    # --------------------------------------------------------
    # Engine noise diagnosis
    # --------------------------------------------------------

    elif (
        (
            "engine" in conversation_text
            or "motor" in conversation_text
            or "rattling" in conversation_text
            or "knocking" in conversation_text
            or "clicking" in conversation_text
            or "grinding" in conversation_text
            or "strange noise" in conversation_text
            or "unusual noise" in conversation_text
            or "weird noise" in conversation_text
        )
        and (
            "noise" in conversation_text
            or "sound" in conversation_text
            or "rattling" in conversation_text
            or "knocking" in conversation_text
            or "clicking" in conversation_text
            or "grinding" in conversation_text
        )
    ):
        problem = "Unusual engine noise"

        diagnosis = (
            "The vehicle appears to have an unusual engine "
            "noise. Possible causes can include a loose or "
            "vibrating component, an exhaust or heat-shield "
            "issue, or another mechanical problem. The exact "
            "cause cannot be confirmed without physical "
            "inspection."
        )

        confidence = "low"

        recommended_service = (
            "Engine inspection"
        )

    # --------------------------------------------------------
    # Oil diagnosis
    # --------------------------------------------------------

    elif "oil" in conversation_text:
        problem = "Oil-related issue"

        diagnosis = (
            "The symptoms may indicate an oil-level, oil-leak, "
            "or oil-pressure-related problem. The oil level and "
            "engine should be inspected."
        )

        confidence = "medium"

        recommended_service = (
            "Engine oil and leak inspection"
        )

    # --------------------------------------------------------
    # AC diagnosis
    # --------------------------------------------------------

    elif (
        "ac" in conversation_text
        or "air conditioning" in conversation_text
        or "air conditioner" in conversation_text
    ):
        problem = "Air conditioning issue"

        diagnosis = (
            "The symptoms suggest a possible air-conditioning "
            "system issue. The refrigerant level, compressor, "
            "condenser, and related components should be checked."
        )

        confidence = "medium"

        recommended_service = (
            "AC inspection and servicing"
        )

    # --------------------------------------------------------
    # General diagnosis
    # --------------------------------------------------------

    else:
        problem = "General vehicle issue"

        diagnosis = (
            "There is not enough information to identify the "
            "exact cause. A mechanic should inspect the vehicle "
            "after collecting more symptoms."
        )

        confidence = "low"

        recommended_service = (
            "General vehicle inspection"
        )

    # --------------------------------------------------------
    # Create or update diagnosis
    # --------------------------------------------------------

    diagnosis_record, created = Diagnosis.objects.update_or_create(
        conversation=conversation,
        defaults={
            "problem": problem,
            "diagnosis": diagnosis,
            "confidence": confidence,
            "recommended_service": recommended_service,
        },
    )

    return Response(
        {
            "success": True,
            "diagnosis_id": diagnosis_record.id,
            "session_id": session_id,
            "problem": diagnosis_record.problem,
            "diagnosis": diagnosis_record.diagnosis,
            "confidence": diagnosis_record.confidence,
            "recommended_service": (
                diagnosis_record.recommended_service
            ),
        },
        status=status.HTTP_200_OK,
    )


# ============================================================
# CREATE BOOKING
# ============================================================

@api_view(["POST"])
def create_booking(request):
    serializer = BookingSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    session_id = serializer.validated_data.get("session_id")

    if not session_id:
        return Response(
            {
                "success": False,
                "error": "session_id is required.",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        conversation = Conversation.objects.get(
            session_id=session_id
        )
    except Conversation.DoesNotExist:
        return Response(
            {
                "success": False,
                "error": "Conversation not found.",
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    try:
        diagnosis = Diagnosis.objects.get(
            conversation=conversation
        )
    except Diagnosis.DoesNotExist:
        return Response(
            {
                "success": False,
                "error": (
                    "Please generate a diagnosis before "
                    "booking a mechanic."
                ),
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    booking = Booking.objects.create(
        diagnosis=diagnosis,
        customer_name=serializer.validated_data["customer_name"],
        phone=serializer.validated_data["phone"],
        car_model=serializer.validated_data["car_model"],
        preferred_date=serializer.validated_data["preferred_date"],
        preferred_time=serializer.validated_data["preferred_time"],
        service=serializer.validated_data["service"],
    )

    return Response(
        {
            "success": True,
            "booking_id": booking.id,
            "status": booking.status,
            "customer_name": booking.customer_name,
            "phone": booking.phone,
            "car_model": booking.car_model,
            "preferred_date": booking.preferred_date,
            "preferred_time": booking.preferred_time,
            "service": booking.service,
            "message": (
                "Mechanic booking created successfully."
            ),
        },
        status=status.HTTP_201_CREATED,
    )


# ============================================================
# GET BOOKING
# ============================================================

@api_view(["GET"])
def get_booking(request, booking_id):
    try:
        booking = Booking.objects.get(
            id=booking_id
        )
    except Booking.DoesNotExist:
        return Response(
            {
                "success": False,
                "error": "Booking not found.",
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    return Response(
        {
            "success": True,
            "booking": {
                "id": booking.id,
                "customer_name": booking.customer_name,
                "phone": booking.phone,
                "car_model": booking.car_model,
                "preferred_date": booking.preferred_date,
                "preferred_time": booking.preferred_time,
                "service": booking.service,
                "status": booking.status,
                "created_at": booking.created_at,
            },
        },
        status=status.HTTP_200_OK,
    )