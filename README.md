🚗 AI Car Mechanic

An AI-powered car troubleshooting and mechanic-booking web application that helps users describe vehicle problems, upload supporting media, receive an AI-assisted diagnosis, and book a mechanic service.

The project is built as a full-stack application using Next.js for the frontend and Django REST Framework for the backend, with SQLite for data persistence.

📌 Project Overview

AI Car Mechanic is designed to provide a simple digital interface for users experiencing car-related problems.

A user can:

Describe a car problem through text
Upload an image, audio recording, or video related to the problem
Interact with the mechanic chatbot
Generate a vehicle diagnosis
View the diagnosed problem
See the confidence level of the diagnosis
Receive a recommended repair/service
Book a mechanic
View booking confirmation and booking details

The application combines conversational interaction, media uploads, AI-assisted diagnosis, and service booking into a single workflow.

✨ Key Features
💬 AI Car Mechanic Chat

Users can describe their vehicle problem using natural language.

Example:

"My car makes a rattling noise when I accelerate."

The chatbot processes the user's message and provides a relevant response.

📷 Image Upload

Users can upload images related to their car problem.

Supported image formats depend on the browser and backend configuration.

Example use cases:

Dashboard warning lights
Visible engine components
Damaged parts
Tyre condition
Exterior damage
🎙️ Audio Upload

Users can upload an audio recording of unusual vehicle sounds.

This can be useful for problems such as:

Rattling
Grinding
Clicking
Squeaking
Knocking
Unusual engine sounds
🎥 Video Upload

Users can upload a video demonstrating a vehicle issue.

This can provide additional context when a problem involves:

Engine behaviour
Visible movement
Smoke
Vibrations
Dashboard indicators
Mechanical sounds
🔍 Vehicle Diagnosis

The application provides a diagnosis workflow based on the user's conversation/session.

The diagnosis interface displays:

Problem
Diagnosis
Confidence
Recommended Service
🧑‍🔧 Mechanic Booking

After receiving a diagnosis, users can select:

Book a Mechanic

The booking form collects:

Customer name
Phone number
Car model
Preferred date
Preferred time
Recommended service

A booking confirmation is then displayed with the generated booking information.

🗂️ Session-Based Conversations

Each conversation is associated with a session ID.

This allows the backend to associate:

Chat messages
Uploaded media
Diagnosis
Booking information

with the relevant user session.

🏗️ System Architecture
                    ┌─────────────────────┐
                    │       User          │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Next.js Frontend  │
                    │                     │
                    │ • Chat Interface    │
                    │ • Media Upload      │
                    │ • Diagnosis UI      │
                    │ • Booking Form      │
                    └──────────┬──────────┘
                               │
                         REST API Calls
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Django REST Backend │
                    │                     │
                    │ • Chat API          │
                    │ • Upload API        │
                    │ • Diagnosis API     │
                    │ • Booking API       │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┴─────────────┐
                 ▼                           ▼
        ┌─────────────────┐        ┌─────────────────┐
        │     SQLite      │        │   AI / Logic    │
        │    Database     │        │    Processing   │
        └─────────────────┘        └─────────────────┘
🔄 Application Workflow
1. Start a Conversation

The user opens the application and starts describing their car problem.

Example:

"My car is making a strange rattling noise when I accelerate."
2. Chat Interaction

The frontend sends the user's message to the Django backend.

Next.js
   ↓
POST /api/chat/
   ↓
Django REST API
   ↓
AI / application logic
   ↓
Response
   ↓
Next.js chatbot
3. Upload Supporting Media

The user can attach an:

Image
Audio file
Video file

The media is uploaded through the backend and associated with the current session.

4. Generate Diagnosis

The diagnosis endpoint processes the current session and returns information such as:

{
  "problem": "Unusual engine noise",
  "diagnosis": "Possible engine-related mechanical issue",
  "confidence": "Low",
  "recommended_service": "Engine inspection"
}

Diagnosis output is intended as an AI-assisted troubleshooting aid and should not replace professional mechanical inspection.

5. Book a Mechanic

The user can proceed to mechanic booking after receiving the recommended service.

The booking request contains:

{
  "session_id": "session-example",
  "customer_name": "Customer Name",
  "phone": "XXXXXXXXXX",
  "car_model": "Hyundai i20",
  "preferred_date": "2026-09-30",
  "preferred_time": "11:00",
  "service": "Engine inspection"
}
6. Booking Confirmation

After successful booking, the application displays:

Booking ID
Customer name
Car model
Date
Time
Booking status
🛠️ Tech Stack
Frontend
Next.js 16.3.6
React
TypeScript
Tailwind CSS
HTML5
CSS
Fetch API
Backend
Python
Django 6.1.1
Django REST Framework
django-cors-headers
Database
SQLite
Development Tools
Git
GitHub
VS Code
npm
Python virtual environment
Deployment
Vercel — frontend deployment
📁 Project Structure
ai-car-mechanic/
│
├── backend/
│   │
│   ├── config/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   └── wsgi.py
│   │
│   ├── mechanic/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── ...
│   │
│   ├── manage.py
│   └── db.sqlite3
│
├── frontend/
│   │
│   ├── app/
│   │   ├── page.tsx
│   │   ├── layout.tsx
│   │   └── ...
│   │
│   ├── public/
│   ├── package.json
│   ├── tsconfig.json
│   └── ...
│
└── README.md
⚙️ Local Installation
Prerequisites

Make sure the following are installed:

Python 3.x
Node.js
npm
Git
🐍 Backend Setup

Navigate to the backend directory:

cd backend
1. Create a virtual environment

Windows:

python -m venv .venv
2. Activate the virtual environment
.venv\Scripts\activate
3. Install Python dependencies
pip install django djangorestframework django-cors-headers

If a requirements.txt file is available, use:

pip install -r requirements.txt
4. Run database migrations
python manage.py makemigrations
python manage.py migrate
5. Start the Django server
python manage.py runserver

The backend will normally be available at:

http://127.0.0.1:8000/
⚛️ Frontend Setup

Open another terminal and navigate to:

cd frontend

Install dependencies:

npm install

Start the development server:

npm run dev

The Next.js application will normally be available at:

http://localhost:3000
🔌 API Endpoints

The application uses REST APIs to communicate between the frontend and backend.

Chat
POST /api/chat/

Sends a user message to the mechanic chatbot.

Example request:

{
  "session_id": "session-example",
  "message": "My car is making a rattling noise."
}
Media Upload
POST /api/upload/

Uploads supporting vehicle media.

Request type:

multipart/form-data

Parameters:

session_id
file

Supported media categories:

Image
Audio
Video
Diagnosis
POST /api/diagnosis/

Generates a diagnosis for the current conversation/session.

Example request:

{
  "session_id": "session-example"
}

Example response:

{
  "problem": "Unusual engine noise",
  "diagnosis": "Possible mechanical issue",
  "confidence": "Low",
  "recommended_service": "Engine inspection",
  "diagnosis_id": 1
}
Booking
POST /api/booking/

Creates a mechanic booking.

Example request:

{
  "session_id": "session-example",
  "customer_name": "Customer Name",
  "phone": "XXXXXXXXXX",
  "car_model": "Hyundai i20",
  "preferred_date": "2026-09-30",
  "preferred_time": "11:00",
  "service": "Engine inspection"
}
Booking Details
GET /api/booking/{id}/

Retrieves information about a specific booking.

This endpoint should be verified against the current backend implementation before claiming it as completed functionality.

🧪 Example User Journey

A typical interaction can look like this:

User
 │
 │ "My car is making a rattling noise while accelerating."
 ▼
AI Car Mechanic
 │
 │ Conversational response
 ▼
User
 │
 │ Uploads supporting media
 ▼
AI Car Mechanic
 │
 │ Diagnosis
 ▼
┌─────────────────────────────┐
│ Problem: Engine noise       │
│ Diagnosis: Possible issue   │
│ Confidence: Low             │
│ Service: Engine inspection  │
└─────────────────────────────┘
 │
 ▼
Book a Mechanic
 │
 ▼
Booking Form
 │
 ▼
Booking Confirmation
🔐 Data & Safety Considerations

The application is designed as a troubleshooting assistant rather than a replacement for professional automotive inspection.

Users should not rely solely on an AI-generated diagnosis for:

Safety-critical mechanical issues
Brake problems
Steering problems
Fuel leaks
Electrical hazards
Engine failures
Other potentially dangerous conditions

A qualified mechanic should inspect the vehicle before carrying out repairs.

🎯 Project Objectives

The project demonstrates the integration of:

Modern frontend development
REST API development
Full-stack application architecture
AI-assisted conversational interfaces
Multimedia file handling
Session-based application workflows
Database-backed booking systems
Frontend/backend integration
Cloud deployment
🚀 Deployment

The frontend has been deployed using Vercel.

The production deployment should be configured so that the frontend communicates with the deployed backend API rather than a local development address.

For local development:

Frontend → http://localhost:3000
Backend  → http://127.0.0.1:8000

For production:

User
 ↓
Vercel / Next.js
 ↓
Production Django REST API
 ↓
Database / AI processing

Before final submission, verify that every production API request points to the deployed backend URL and not 127.0.0.1.

📋 Current Feature Checklist
Feature	Status
Next.js frontend	✅
React-based UI	✅
Django backend	✅
Django REST Framework	✅
SQLite database	✅
Text chat	✅
Image upload	✅
Audio upload	✅
Video upload	✅
Session-based interaction	✅
Diagnosis workflow	✅
Diagnosis confidence	✅
Recommended service	✅
Mechanic booking	✅
Booking confirmation	✅
GitHub repository	✅
Vercel frontend deployment	✅
Production backend verification	🔄
Booking GET endpoint verification	🔄
Irrelevant/non-car query handling	🔄
Follow-up questions before diagnosis	🔄
Actual media analysis	🔄
Final API documentation verification	🔄

The items marked 🔄 should be verified against the final backend implementation before describing them as completed.

🔮 Future Improvements

Potential future enhancements include:

Authentication and user accounts
Persistent conversation history
Mechanic/admin dashboard
Real-time booking status
Mechanic location tracking
More detailed vehicle-specific troubleshooting
AI-powered image analysis
Audio-based car sound analysis
Video-based issue detection
Service-center integration
Email/SMS booking notifications
Cloud database
Production-grade file storage
Improved diagnosis confidence scoring
Advanced safety warnings
💡 Why This Project?

Traditional vehicle troubleshooting often requires users to understand mechanical terminology before they can explain a problem.

AI Car Mechanic provides a conversational interface that allows users to describe symptoms in everyday language and receive structured troubleshooting guidance.

The application combines:

Conversation → Media → Diagnosis → Service Recommendation → Mechanic Booking

into a single workflow.

👩‍💻 Developer

Aditi Dwivedi

Full-Stack / Software Development Project

Technologies

Next.js · React · TypeScript · Tailwind CSS · Python · Django · Django REST Framework · SQLite · REST APIs · Git · GitHub

📄 Project Status

This project was developed as a full-stack AI application demonstrating conversational troubleshooting, multimedia input, diagnosis, and mechanic booking.

The final backend implementation and production configuration should be verified before submission to ensure all task requirements are fully satisfied.
