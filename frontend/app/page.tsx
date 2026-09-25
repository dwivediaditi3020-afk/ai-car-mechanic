"use client";

import { ChangeEvent, FormEvent, useRef, useState } from "react";

const API_BASE_URL = "";

type Message = {
  id: number;
  sender: "user" | "bot";
  message: string;
  media_url?: string;
  media_type?: "image" | "audio" | "video";
};

type Diagnosis = {
  diagnosis_id: number;
  problem: string;
  diagnosis: string;
  confidence: string;
  recommended_service: string;
};

type Booking = {
  booking_id: number;
  customer_name: string;
  phone: string;
  car_model: string;
  preferred_date: string;
  preferred_time: string;
  service: string;
  status: string;
};

export default function Home() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [uploadLoading, setUploadLoading] = useState(false);
  const [hasUploadedMedia, setHasUploadedMedia] = useState(false);

  const [diagnosis, setDiagnosis] = useState<Diagnosis | null>(null);
  const [diagnosisLoading, setDiagnosisLoading] = useState(false);

  const [booking, setBooking] = useState<Booking | null>(null);
  const [bookingLoading, setBookingLoading] = useState(false);

  const [customerName, setCustomerName] = useState("");
  const [phone, setPhone] = useState("");
  const [carModel, setCarModel] = useState("");
  const [preferredDate, setPreferredDate] = useState("");
  const [preferredTime, setPreferredTime] = useState("");

  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const [sessionId] = useState(() => `session-${Date.now()}`);

  const sendMessage = async () => {
    const userMessage = input.trim();

    if (!userMessage || loading) {
      return;
    }

    setLoading(true);

    const userMessageObject: Message = {
      id: Date.now(),
      sender: "user",
      message: userMessage,
    };

    setMessages((prev) => [...prev, userMessageObject]);
    setInput("");

    try {
      const response = await fetch(`${API_BASE_URL}/api/chat/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          session_id: sessionId,
          message: userMessage,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data?.error ||
          data?.errors ||
          JSON.stringify(data) ||
          "Failed to send message."
        );
      }

      const botMessageObject: Message = {
        id: Date.now() + 1,
        sender: "bot",
        message:
          data?.reply ||
          data?.message ||
          "I received your message.",
      };

      setMessages((prev) => [...prev, botMessageObject]);
    } catch (error) {
      console.error("Chat error:", error);

      const errorMessage: Message = {
        id: Date.now() + 1,
        sender: "bot",
        message:
          error instanceof Error
            ? error.message
            : "Something went wrong while contacting the mechanic.",
      };

      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    sendMessage();
  };

  const handleFileChange = async (
    event: ChangeEvent<HTMLInputElement>
  ) => {
    const file = event.target.files?.[0];

    if (!file || uploadLoading) {
      return;
    }

    setUploadLoading(true);

    try {
      const formData = new FormData();

      formData.append("session_id", sessionId);
      formData.append("file", file);

      const response = await fetch(`${API_BASE_URL}/api/upload/`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data?.error ||
          data?.errors ||
          JSON.stringify(data) ||
          "Failed to upload media."
        );
      }

      const mediaUrl = data.media_url?.startsWith("http")
        ? data.media_url
        : `${API_BASE_URL}${data.media_url}`;

      const mediaMessage: Message = {
        id: Date.now(),
        sender: "user",
        message: file.name,
        media_url: mediaUrl,
        media_type: data.media_type,
      };

      setMessages((prev) => [...prev, mediaMessage]);
      setHasUploadedMedia(true);
    } catch (error) {
      console.error("Upload error:", error);

      const errorMessage: Message = {
        id: Date.now(),
        sender: "bot",
        message:
          error instanceof Error
            ? error.message
            : "Something went wrong while uploading the file.",
      };

      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setUploadLoading(false);

      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }
    }
  };

  const generateDiagnosis = async () => {
    if (diagnosisLoading) {
      return;
    }

    setDiagnosisLoading(true);

    try {
      const response = await fetch(
        `${API_BASE_URL}/api/diagnosis/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            session_id: sessionId,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data?.error ||
          data?.errors ||
          JSON.stringify(data) ||
          "Failed to generate diagnosis."
        );
      }

      setDiagnosis(data);
      setBooking(null);
    } catch (error) {
      console.error("Diagnosis error:", error);

      alert(
        error instanceof Error
          ? error.message
          : "Failed to generate diagnosis."
      );
    } finally {
      setDiagnosisLoading(false);
    }
  };

  const createBooking = async () => {
    if (!diagnosis || bookingLoading) {
      return;
    }

    if (
      !customerName.trim() ||
      !phone.trim() ||
      !carModel.trim() ||
      !preferredDate ||
      !preferredTime
    ) {
      alert("Please fill all booking details.");
      return;
    }

    setBookingLoading(true);

    try {
      const response = await fetch(
        `${API_BASE_URL}/api/booking/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            session_id: sessionId,
            customer_name: customerName,
            phone: phone,
            car_model: carModel,
            preferred_date: preferredDate,
            preferred_time: preferredTime,
            service: diagnosis.recommended_service,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        console.error("Booking API response:", data);

        throw new Error(
          data?.error ||
          data?.errors ||
          JSON.stringify(data) ||
          "Failed to create booking."
        );
      }

      setBooking(data);
    } catch (error) {
      console.error("Booking error:", error);

      alert(
        error instanceof Error
          ? error.message
          : "Failed to create booking."
      );
    } finally {
      setBookingLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gray-100 px-4 py-8">
      <div className="mx-auto max-w-5xl">
        <div className="mb-6 text-center">
          <h1 className="text-3xl font-bold text-gray-900">
            AI Car Mechanic
          </h1>

          <p className="mt-2 text-gray-600">
            Chat with your virtual mechanic for car troubleshooting
            and diagnosis.
          </p>
        </div>

        <div className="grid gap-6 lg:grid-cols-3">
          {/* CHAT SECTION */}
          <section className="rounded-xl bg-white p-5 shadow lg:col-span-2">
            <h2 className="mb-4 text-xl font-semibold text-gray-900">
              Mechanic Chat
            </h2>

            <div className="mb-4 h-[500px] overflow-y-auto rounded-lg border bg-gray-50 p-4">
              {messages.length === 0 ? (
                <div className="flex h-full items-center justify-center text-center text-gray-500">
                  <div>
                    <p className="font-medium">
                      Tell me what is wrong with your car.
                    </p>

                    <p className="mt-2 text-sm">
                      You can describe the issue or upload an image,
                      audio, or video.
                    </p>
                  </div>
                </div>
              ) : (
                <div className="space-y-4">
                  {messages.map((message) => (
                    <div
                      key={message.id}
                      className={`flex ${message.sender === "user"
                          ? "justify-end"
                          : "justify-start"
                        }`}
                    >
                      <div
                        className={`max-w-[80%] rounded-lg px-4 py-3 ${message.sender === "user"
                            ? "bg-blue-600 text-white"
                            : "bg-white text-gray-900 shadow"
                          }`}
                      >
                        {message.media_type === "image" &&
                          message.media_url ? (
                          <div>
                            <img
                              src={message.media_url}
                              alt={message.message}
                              className="max-h-64 rounded-lg object-contain"
                            />

                            <p className="mt-2 text-sm">
                              {message.message}
                            </p>
                          </div>
                        ) : message.media_type === "audio" &&
                          message.media_url ? (
                          <div>
                            <audio
                              controls
                              src={message.media_url}
                              className="max-w-full"
                            />

                            <p className="mt-2 text-sm">
                              {message.message}
                            </p>
                          </div>
                        ) : message.media_type === "video" &&
                          message.media_url ? (
                          <div>
                            <video
                              controls
                              src={message.media_url}
                              className="max-h-72 max-w-full rounded-lg"
                            />

                            <p className="mt-2 text-sm">
                              {message.message}
                            </p>
                          </div>
                        ) : (
                          <p className="whitespace-pre-wrap">
                            {message.message}
                          </p>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            <form
              onSubmit={handleSubmit}
              className="flex flex-col gap-3"
            >
              <textarea
                value={input}
                onChange={(event) =>
                  setInput(event.target.value)
                }
                onKeyDown={(event) => {
                  if (event.key === "Enter" && !event.shiftKey) {
                    event.preventDefault();
                    sendMessage();
                  }
                }}
                placeholder="Describe your car problem..."
                rows={3}
                className="w-full resize-none rounded-lg border border-gray-300 p-3 text-gray-900 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
              />

              <div className="flex flex-wrap gap-3">
                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/*,audio/*,video/*"
                  onChange={handleFileChange}
                  className="hidden"
                />

                <button
                  type="button"
                  onClick={() => fileInputRef.current?.click()}
                  disabled={uploadLoading}
                  className="rounded-lg border border-gray-300 px-4 py-2 font-medium text-gray-700 hover:bg-gray-100 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  {uploadLoading
                    ? "Uploading..."
                    : "Upload Media"}
                </button>

                <button
                  type="submit"
                  disabled={
                    loading ||
                    uploadLoading ||
                    !input.trim()
                  }
                  className="rounded-lg bg-blue-600 px-5 py-2 font-medium text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  {loading ? "Sending..." : "Send"}
                </button>
              </div>
            </form>

            {(messages.length > 0 || hasUploadedMedia) && (
              <div className="mt-5">
                <button
                  type="button"
                  onClick={generateDiagnosis}
                  disabled={
                    diagnosisLoading ||
                    loading ||
                    uploadLoading
                  }
                  className="w-full rounded-lg bg-green-600 px-5 py-3 font-semibold text-white hover:bg-green-700 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  {diagnosisLoading
                    ? "Generating Diagnosis..."
                    : "Generate Diagnosis"}
                </button>
              </div>
            )}
          </section>

          {/* DIAGNOSIS + BOOKING */}
          <section className="space-y-6">
            {diagnosis && (
              <div className="rounded-xl bg-white p-5 shadow">
                <h2 className="mb-4 text-xl font-semibold text-gray-900">
                  Diagnosis
                </h2>

                <div className="space-y-3 text-sm">
                  <div>
                    <p className="font-semibold text-gray-500">
                      Problem
                    </p>

                    <p className="text-gray-900">
                      {diagnosis.problem}
                    </p>
                  </div>

                  <div>
                    <p className="font-semibold text-gray-500">
                      Diagnosis
                    </p>

                    <p className="text-gray-900">
                      {diagnosis.diagnosis}
                    </p>
                  </div>

                  <div>
                    <p className="font-semibold text-gray-500">
                      Confidence
                    </p>

                    <p className="text-gray-900">
                      {diagnosis.confidence}
                    </p>
                  </div>

                  <div>
                    <p className="font-semibold text-gray-500">
                      Recommended Service
                    </p>

                    <p className="text-gray-900">
                      {diagnosis.recommended_service}
                    </p>
                  </div>
                </div>
              </div>
            )}

            {diagnosis && !booking && (
              <div className="rounded-xl bg-white p-5 shadow">
                <h2 className="mb-4 text-xl font-semibold text-gray-900">
                  Book Mechanic
                </h2>

                <div className="space-y-3">
                  <input
                    type="text"
                    placeholder="Customer name"
                    value={customerName}
                    onChange={(event) =>
                      setCustomerName(event.target.value)
                    }
                    className="w-full rounded-lg border border-gray-300 p-3 text-gray-900 outline-none focus:border-blue-500"
                  />

                  <input
                    type="tel"
                    placeholder="Phone number"
                    value={phone}
                    onChange={(event) =>
                      setPhone(event.target.value)
                    }
                    className="w-full rounded-lg border border-gray-300 p-3 text-gray-900 outline-none focus:border-blue-500"
                  />

                  <input
                    type="text"
                    placeholder="Car model"
                    value={carModel}
                    onChange={(event) =>
                      setCarModel(event.target.value)
                    }
                    className="w-full rounded-lg border border-gray-300 p-3 text-gray-900 outline-none focus:border-blue-500"
                  />

                  <input
                    type="date"
                    value={preferredDate}
                    onChange={(event) =>
                      setPreferredDate(event.target.value)
                    }
                    className="w-full rounded-lg border border-gray-300 p-3 text-gray-900 outline-none focus:border-blue-500"
                  />

                  <input
                    type="time"
                    value={preferredTime}
                    onChange={(event) =>
                      setPreferredTime(event.target.value)
                    }
                    className="w-full rounded-lg border border-gray-300 p-3 text-gray-900 outline-none focus:border-blue-500"
                  />

                  <button
                    type="button"
                    onClick={createBooking}
                    disabled={bookingLoading}
                    className="w-full rounded-lg bg-orange-600 px-5 py-3 font-semibold text-white hover:bg-orange-700 disabled:cursor-not-allowed disabled:opacity-50"
                  >
                    {bookingLoading
                      ? "Booking..."
                      : "Book Mechanic"}
                  </button>
                </div>
              </div>
            )}

            {booking && (
              <div className="rounded-xl bg-white p-5 shadow">
                <h2 className="mb-4 text-xl font-semibold text-green-700">
                  Booking Confirmed
                </h2>

                <div className="space-y-2 text-sm text-gray-900">
                  <p>
                    <strong>Booking ID:</strong>{" "}
                    #{booking.booking_id}
                  </p>

                  <p>
                    <strong>Name:</strong>{" "}
                    {booking.customer_name}
                  </p>

                  <p>
                    <strong>Phone:</strong>{" "}
                    {booking.phone}
                  </p>

                  <p>
                    <strong>Car:</strong>{" "}
                    {booking.car_model}
                  </p>

                  <p>
                    <strong>Date:</strong>{" "}
                    {booking.preferred_date}
                  </p>

                  <p>
                    <strong>Time:</strong>{" "}
                    {booking.preferred_time}
                  </p>

                  <p>
                    <strong>Service:</strong>{" "}
                    {booking.service}
                  </p>

                  <p>
                    <strong>Status:</strong>{" "}
                    {booking.status}
                  </p>
                </div>

                <p className="mt-4 rounded-lg bg-green-50 p-3 text-sm text-green-800">
                  Mechanic booking created successfully.
                </p>
              </div>
            )}
          </section>
        </div>
      </div>
    </main>
  );
}