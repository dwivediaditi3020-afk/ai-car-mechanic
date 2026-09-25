# 🚗 AI Car Mechanic

### AI-Powered Car Troubleshooting, Diagnosis & Mechanic Booking Platform

AI Car Mechanic is a full-stack web application that works as a virtual automobile mechanic. Users can describe their vehicle problems through an interactive chatbot, answer troubleshooting questions, upload vehicle images, audio, or video, receive a structured diagnosis with recommended service, and book a mechanic appointment.

The application combines **Next.js, React, Django REST Framework, SQLite, and Google Gemini multimodal AI** to provide an end-to-end automobile troubleshooting and booking experience.

---

## 🌐 Live Demo

### Frontend

**https://ai-car-mechanic-nine.vercel.app/**

### Backend API

**http://ai-car-mechanic-env.eba-mrgpjfrd.ap-south-1.elasticbeanstalk.com/**

### GitHub Repository

**https://github.com/dwivediaditi3020-afk/ai-car-mechanic**

---

## 📌 Project Overview

The AI Car Mechanic platform is designed to provide users with an accessible first-level automobile troubleshooting experience.

The system allows users to:

1. Start a conversation with the virtual mechanic.
2. Describe their vehicle problem.
3. Answer follow-up troubleshooting questions.
4. Upload vehicle-related images, audio, or video.
5. Receive AI-powered observations from uploaded media.
6. Generate a structured vehicle diagnosis.
7. View the recommended service.
8. Book a mechanic appointment.
9. Receive booking confirmation and booking details.

The application combines traditional backend troubleshooting logic with AI-powered multimodal analysis to create an efficient and practical workflow.

---

# ✨ Features

## 🤖 Virtual Mechanic Chatbot

* Interactive conversational mechanic interface
* Vehicle troubleshooting through natural-language chat
* Context-aware follow-up questions
* Automotive-focused responses
* Structured troubleshooting workflow
* Car-related query handling
* Unrelated query handling

---

## 🔧 Automotive Troubleshooting

The chatbot supports common automotive problem categories including:

* Engine problems
* Unusual engine noises
* Brake problems
* Battery and starting issues
* Overheating
* Tyre problems
* Oil-related issues
* Air-conditioning problems
* General mechanical symptoms

The backend uses structured troubleshooting logic to efficiently handle common automotive scenarios.

---

## 📷 Multimedia Uploads

Users can upload vehicle-related media directly from the chat interface.

### Supported Media

* 🖼️ Images
* 🎵 Audio
* 🎥 Video

Uploaded media is associated with the user's active conversation and can be used as part of the diagnosis workflow.

---

## 🧠 Gemini-Powered Media Analysis

Google Gemini multimodal AI is integrated for analyzing uploaded vehicle media.

The analysis focuses on automotive observations such as:

* Visible vehicle damage
* Abnormal components
* Warning indicators
* Mechanical symptoms
* Unusual sounds
* Possible mechanical causes
* Areas requiring mechanic inspection

The resulting observations are incorporated into the diagnosis workflow.

---

## 🩺 Structured Diagnosis

The system generates a structured diagnosis containing:

* **Problem**
* **Diagnosis**
* **Confidence**
* **Recommended Service**

This provides users with a clear summary of the troubleshooting conversation.

---

## 📅 Mechanic Booking

Users can proceed from diagnosis to mechanic booking.

The booking form collects:

* Customer name
* Phone number
* Car model
* Preferred date
* Preferred time
* Recommended service

A unique booking ID is generated for every booking.

---

## 📋 Booking Retrieval

Existing booking information can be retrieved using the booking ID.

This provides access to:

* Customer information
* Vehicle information
* Appointment details
* Requested service
* Booking status

---

## 💬 Modern Chat Experience

The frontend provides:

* Conversation history
* User and mechanic messages
* Image previews
* Audio uploads
* Video uploads
* Diagnosis display
* Booking workflow
* Booking confirmation
* Loading states
* Error handling
* Enter-to-send
* Shift + Enter for multiline messages

---

# 🏗️ System Architecture

```text
                         ┌──────────────────────┐
                         │        USER          │
                         │   Web Application    │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   Next.js Frontend   │
                         │       Vercel         │
                         └──────────┬───────────┘
                                    │
                              REST API Requests
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   Django REST API    │
                         │   AWS Elastic        │
                         │      Beanstalk       │
                         └───────┬───────┬──────┘
                                 │       │
                    ┌────────────┘       └─────────────┐
                    ▼                                  ▼
          ┌──────────────────┐              ┌──────────────────┐
          │      SQLite      │              │   Google Gemini  │
          │     Database     │              │ Multimodal AI    │
          └──────────────────┘              └──────────────────┘
                    │                                  │
                    ▼                                  ▼
             Conversations                       Media Analysis
             Messages                           Vehicle Insights
             Diagnoses
             Bookings
```

---

# 🔄 Application Workflow

```text
User
 │
 ▼
Open AI Car Mechanic
 │
 ▼
Start Conversation
 │
 ▼
Describe Vehicle Problem
 │
 ▼
Virtual Mechanic
 │
 ├── Ask Follow-up Questions
 │
 └── Receive Additional Information
 │
 ▼
Upload Vehicle Media
 │
 ├── Image
 ├── Audio
 └── Video
 │
 ▼
Gemini Media Analysis
 │
 ▼
Structured Diagnosis
 │
 ├── Problem
 ├── Diagnosis
 ├── Confidence
 └── Recommended Service
 │
 ▼
Book Mechanic
 │
 ▼
Booking Created
 │
 ▼
Booking Confirmation
```

---

# 🛠️ Technology Stack

## Frontend

| Technology         | Purpose               |
| ------------------ | --------------------- |
| Next.js            | Frontend framework    |
| React              | UI development        |
| TypeScript         | Type-safe development |
| Tailwind CSS       | Styling               |
| Next.js App Router | Application routing   |
| ESLint             | Code quality          |

## Backend

| Technology            | Purpose                      |
| --------------------- | ---------------------------- |
| Python                | Backend programming language |
| Django                | Web framework                |
| Django REST Framework | REST API development         |
| django-cors-headers   | CORS handling                |
| Pillow                | Image processing             |
| SQLite                | Database                     |

## AI

| Technology       | Purpose                           |
| ---------------- | --------------------------------- |
| Google Gemini    | Multimodal vehicle media analysis |
| Google GenAI SDK | Gemini API integration            |

## Deployment

| Platform              | Component        |
| --------------------- | ---------------- |
| Vercel                | Next.js frontend |
| AWS Elastic Beanstalk | Django backend   |

---

# 📡 REST API Documentation

## 1. Chat API

### `POST /api/chat/`

Handles the virtual mechanic conversation.

### Request

```json
{
  "session_id": "unique-session-id",
  "message": "My car is making a rattling noise during acceleration"
}
```

### Response

```json
{
  "reply": "..."
}
```

---

# 2. Media Upload API

### `POST /api/upload/`

Uploads vehicle-related image, audio, or video files.

### Request

Multipart form data:

```text
session_id
file
```

### Response

Returns the uploaded media information and media URL.

---

# 3. Diagnosis API

### `POST /api/diagnosis/`

Generates a structured vehicle diagnosis based on the conversation and available media.

### Request

```json
{
  "session_id": "unique-session-id"
}
```

### Response

```json
{
  "problem": "...",
  "diagnosis": "...",
  "confidence": "...",
  "recommended_service": "..."
}
```

---

# 4. Booking API

### `POST /api/booking/`

Creates a mechanic service booking.

### Request

```json
{
  "session_id": "unique-session-id",
  "customer_name": "Customer Name",
  "phone": "9876543210",
  "car_model": "Hyundai i20",
  "preferred_date": "2026-09-30",
  "preferred_time": "11:00",
  "service": "Mechanic inspection"
}
```

### Response

Returns the created booking details and booking ID.

---

# 5. Booking Details API

### `GET /api/booking/{id}/`

Retrieves an existing mechanic booking.

### Example

```text
GET /api/booking/1/
```

---

# 🗄️ Database Design

The application uses SQLite for persistent application data.

### Conversation

Stores individual user conversation sessions.

### Message

Stores:

* Conversation messages
* User messages
* Mechanic responses
* Uploaded media
* Media types

### Diagnosis

Stores:

* Vehicle problem
* Diagnosis
* Confidence
* Recommended service
* Related conversation

### Booking

Stores:

* Customer information
* Vehicle information
* Appointment details
* Requested service
* Booking status
* Related conversation
* Related diagnosis

---

# 📁 Project Structure

```text
ai-car-mechanic/
│
├── backend/
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   └── wsgi.py
│   │
│   ├── mechanic/
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   │
│   ├── .ebextensions/
│   │   └── django.config
│   │
│   ├── .platform/
│   │   └── nginx/
│   │
│   ├── manage.py
│   └── requirements.txt
│
├── frontend/
│   │
│   ├── app/
│   │   ├── favicon.ico
│   │   ├── globals.css
│   │   ├── layout.tsx
│   │   └── page.tsx
│   │
│   ├── public/
│   ├── package.json
│   ├── package-lock.json
│   ├── next.config.ts
│   ├── postcss.config.mjs
│   ├── eslint.config.mjs
│   └── tsconfig.json
│
├── .gitignore
└── README.md
```

---

# 🚀 Installation & Local Development

## Prerequisites

Make sure the following are installed:

* Python 3.x
* Node.js
* npm
* Git

---

## Backend Setup

Open a terminal and navigate to:

```bash
cd ai-car-mechanic/backend
```

Create a virtual environment:

### Windows

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Run database migrations:

```bash
python manage.py migrate
```

Start the backend:

```bash
python manage.py runserver
```

Backend:

```text
http://127.0.0.1:8000/
```

---

# 🎨 Frontend Setup

Open another terminal.

Navigate to:

```bash
cd ai-car-mechanic/frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Frontend:

```text
http://localhost:3000/
```

---

# 🔐 Environment Variables

Create a `.env` file inside the `backend` directory.

```env
DJANGO_SECRET_KEY=your_django_secret_key
GEMINI_API_KEY=your_gemini_api_key
```

### Important

Environment files containing secrets should never be committed to GitHub.

The project `.gitignore` excludes environment files and other sensitive/local development files.

---

# 🧪 Testing

The application has been tested across the major workflows:

* Chat interaction
* Automotive troubleshooting
* Follow-up questions
* Car-related query handling
* Image upload
* Audio upload
* Video upload
* Media preview
* Gemini media analysis
* Diagnosis generation
* Recommended service
* Mechanic booking
* Booking confirmation
* Booking retrieval
* Enter-to-send
* Shift + Enter multiline messaging
* Frontend/backend integration
* Production deployment

---

# 🏭 Production Build

To create a production build of the frontend:

```bash
npm run build
```

The production frontend is deployed using Vercel.

The Django REST backend is deployed using AWS Elastic Beanstalk.

---

# ☁️ Deployment

## Frontend — Vercel

The Next.js frontend is deployed on Vercel.

### Live URL

```text
https://ai-car-mechanic-nine.vercel.app/
```

---

## Backend — AWS Elastic Beanstalk

The Django REST API is deployed using AWS Elastic Beanstalk.

### API URL

```text
http://ai-car-mechanic-env.eba-mrgpjfrd.ap-south-1.elasticbeanstalk.com/
```

---

# 🧠 AI Architecture

The application uses a hybrid approach combining deterministic backend logic with multimodal AI.

### Backend Logic

Traditional backend logic handles common automotive troubleshooting scenarios and conversational flows.

### Gemini AI

Gemini is used for uploaded vehicle media where multimodal analysis provides additional technical observations.

### Diagnosis

The diagnosis workflow combines:

```text
Conversation
     +
Follow-up Information
     +
Uploaded Media
     +
Gemini Analysis
     ↓
Structured Diagnosis
     ↓
Recommended Service
```

This provides an efficient architecture while using AI where it adds value to the application's functionality.

---

# 📂 Media Processing

The media workflow follows:

```text
User Upload
     ↓
Frontend
     ↓
Django Upload API
     ↓
Media Validation
     ↓
Conversation Association
     ↓
Media Storage
     ↓
Gemini Analysis
     ↓
Technical Observation
     ↓
Diagnosis
```

Supported media categories:

* Image
* Audio
* Video

---

# 🛡️ Security

The project follows secure development practices including:

* Environment variables for sensitive credentials
* API keys excluded from source control
* Django secret key stored through environment configuration
* `.gitignore` protection
* Backend request validation
* Media validation
* Production configuration
* CORS configuration
* API input validation

---

# ⚡ Error Handling

The application provides error handling across the major workflows.

This includes:

* Invalid requests
* Missing conversation sessions
* Invalid media uploads
* Unsupported media
* Diagnosis errors
* Booking validation errors
* API request errors
* Frontend request failures
* Loading states
* User-facing error messages

---

# 📱 User Experience

The frontend is designed around a simple conversational workflow.

Users can:

* Start chatting immediately
* Send messages using Enter
* Create multiline messages using Shift + Enter
* Upload vehicle media
* Preview supported media
* Review diagnosis information
* Proceed directly to mechanic booking
* Receive booking confirmation

---

# 📊 Complete Feature Set

| Feature                    | Status |
| -------------------------- | ------ |
| Virtual Mechanic Chatbot   | ✅      |
| Automotive Troubleshooting | ✅      |
| Follow-up Questions        | ✅      |
| Car Query Handling         | ✅      |
| Image Upload               | ✅      |
| Audio Upload               | ✅      |
| Video Upload               | ✅      |
| Media Preview              | ✅      |
| Gemini Media Analysis      | ✅      |
| Structured Diagnosis       | ✅      |
| Confidence Information     | ✅      |
| Recommended Service        | ✅      |
| Mechanic Booking           | ✅      |
| Booking Confirmation       | ✅      |
| Booking Retrieval          | ✅      |
| Conversation Management    | ✅      |
| SQLite Database            | ✅      |
| REST APIs                  | ✅      |
| Error Handling             | ✅      |
| Production Deployment      | ✅      |
| Vercel Frontend            | ✅      |
| AWS Backend                | ✅      |

---

# 👨‍💻 Developer

## Aditi Dwivedi

**Full-Stack Developer | BCA Graduate | MCA Student**

### Technical Interests

* Full-Stack Web Development
* Backend Development
* REST API Development
* AI & Generative AI
* Database Development
* Software Engineering
* Modern Web Applications

### Technologies Used

```text
JavaScript
TypeScript
Python
React
Next.js
Django
Django REST Framework
Node.js
SQL
MongoDB
SQLite
Git
GitHub
REST APIs
Google Gemini
```

---

# 🎯 Project Objectives

The project was developed to demonstrate practical implementation of:

* Full-stack application development
* REST API architecture
* Conversational interfaces
* AI integration
* Multimodal media processing
* Database design
* File upload handling
* Diagnosis workflows
* Booking workflows
* Frontend/backend integration
* Cloud deployment
* Production-oriented development

---

# 📚 Learning Outcomes

This project demonstrates hands-on experience with:

* Next.js application development
* React component development
* TypeScript
* Django REST API development
* API integration
* SQLite database management
* File and media handling
* Gemini API integration
* Multimodal AI workflows
* Frontend/backend communication
* Environment configuration
* Git and GitHub
* Vercel deployment
* AWS Elastic Beanstalk deployment
* Production testing

---

# 📌 Project Deliverables

### GitHub Repository

https://github.com/dwivediaditi3020-afk/ai-car-mechanic

### Live Frontend

https://ai-car-mechanic-nine.vercel.app/

### Live Backend

http://ai-car-mechanic-env.eba-mrgpjfrd.ap-south-1.elasticbeanstalk.com/

---

# 📄 License

This project was developed as a full-stack developer internship assignment and portfolio project.

---

# ⭐ Project Summary

**AI Car Mechanic** is a complete full-stack automobile troubleshooting platform combining:

**Next.js + React + TypeScript + Django + Django REST Framework + SQLite + Google Gemini + Vercel + AWS Elastic Beanstalk**

The application provides a complete journey from:

**Vehicle Problem → Conversation → Follow-up Questions → Media Analysis → Diagnosis → Recommended Service → Mechanic Booking**

---

## 👨‍💻 Developed by

**Aditi Dwivedi**

**AI Car Mechanic — Full-Stack Developer Project**
