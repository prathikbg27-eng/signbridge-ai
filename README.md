# 🤟 SignBridge AI

### Speak. Sign. Understand.

**SignBridge AI** is an AI-powered accessibility and communication platform designed to help bridge communication between hearing and Deaf users through **speech, text, Indian Sign Language (ISL), hand-based sign recognition, and a realistic 3D human avatar**.

The long-term vision is to create a two-way communication assistant:

```text
Speech / Text
     ↓
AI Understanding
     ↓
ISL Gloss
     ↓
3D Human Avatar
     ↓
Sign-based Communication
```

and:

```text
ISL Hand Gesture
     ↓
Hand Landmark Detection
     ↓
Sign Recognition
     ↓
AI Understanding
     ↓
Text / Voice Response
     ↓
3D Avatar Response
```

---

# ✨ Features

## 🎙️ Multilingual Speech Input

SignBridge supports speech input with multilingual processing.

Supported input languages currently include:

* English
* Hindi
* Kannada
* Tamil
* Telugu
* Malayalam
* Gujarati

The current speech pipeline supports language selection/auto-detection and uses speech recognition with a Whisper fallback architecture.

---

## 📝 Text-to-ISL Translation

Users can enter a sentence in the application and convert it into an ISL-oriented gloss sequence.

Example:

```text
Input:
"Where is the hospital?"

↓

Meaning:
Location / hospital inquiry

↓

ISL Gloss:
ME → HOSPITAL → WHERE

↓

3D Avatar:
Performs the corresponding sign sequence
```

The system is designed around a semantic meaning layer rather than simply matching every English word directly to an animation.

---

## 👤 Realistic 3D Human ISL Avatar

SignBridge uses a **Three.js/WebGL 3D human avatar** for visual communication.

The avatar experience is designed to support:

* Sign sequences
* Playback
* Pause
* Replay
* Previous / next
* Adjustable signing speed
* Natural idle state
* Sign-by-sign progress
* Human-like movement
* Future animation retargeting
* Context-aware avatar responses

The objective is for the avatar to behave like a **digital human interpreter**, not a generic game character.

---

## 🤟 Hands-Only Sign Recognition

SignBridge is being developed with a **hands-only sign recognition pipeline**.

The intended flow is:

```text
Webcam
  ↓
Hand Detection
  ↓
21 Hand Landmarks
  ↓
Hand Shape + Orientation
  ↓
Movement Over Time
  ↓
Temporal Sign Recognition
  ↓
ISL Sign
```

The recognition pipeline is intentionally focused on:

* Left hand
* Right hand
* Finger positions
* Wrist
* Palm orientation
* Hand movement
* Temporal gesture patterns

The user's face and body are not intended to be used as recognition inputs in this hands-only mode.

---

# 💬 Two-Way Communication

One of the key goals of SignBridge AI is to move beyond one-way translation.

### User → SignBridge

```text
🤟 User performs HI

↓

AI recognizes:
HELLO

↓

Response:
"Hello! What's up?"

↓

Optional:
Voice response

↓

Optional:
3D avatar signs the response
```

### Speech/Text User → Deaf User

```text
"Where is the hospital?"

↓

AI understanding

↓

ISL gloss

↓

3D avatar performs signs
```

This creates a two-way communication model rather than a simple dictionary.

---

# 🧠 Context-Aware Conversation

SignBridge is designed to understand a sign in the context of the current conversation.

For example:

```text
Avatar:
"Would you like some water?"

User:
🤟 YES

↓

AI understands:

YES + WATER OFFER

↓

Response:

"Sure, I'll get you some."
```

Instead of always returning:

```text
"OK"
```

the response engine is designed to consider:

* Previous conversation
* Pending question
* Current topic
* Recognized sign
* User intent
* Conversation history

---

# 🧩 ISL Meaning Layer

The current application uses a semantic meaning layer to normalize phrases and map them to ISL concepts.

Examples include concepts such as:

```text
HELLO
WHAT
WHERE
HOW
YOU
ME
WATER
HELP
THANK_YOU
PLEASE
YES
NO
NAME
FOOD
FRIEND
HOSPITAL
DOCTOR
TIME
HOME
GOOD
BAD
HAPPY
SAD
STOP
```

The long-term objective is to expand this into a structured **500+ real ISL concept registry**.

---

# 📚 ISL Sign Database

The current prototype includes a CSV-based sign database.

Current prototype structure:

```text
word
sign
category
```

The database is currently used as a vocabulary/reference layer.

Future production architecture will separate:

```text
ISL Vocabulary
       │
       ├── Recognition Data
       │
       └── Avatar Animation Assets
```

This distinction is important.

A sign can exist in the vocabulary without necessarily having:

* a recognition training class
* a 3D avatar animation

The system must never claim an animation exists unless a genuine animation asset exists.

---

# 🎯 500+ ISL Sign Roadmap

The project is being designed to support:

**500+ unique ISL concepts**

The project will not artificially reach 500 by:

* Counting synonyms as separate signs
* Reusing unrelated animations
* Inventing gestures
* Creating fake animation files
* Claiming unsupported recognition

The intended structure is:

```text
500+ verified ISL concepts
        ↓
Actual recognition classes
        ↓
Actual avatar animations
```

These may have different counts during development.

For example:

```text
Vocabulary:
500+

Recognition:
Actual trained classes

Avatar animations:
Actual available assets
```

---

# 🗃️ Planned Production Data Model

The production version is planned around a structured sign registry.

A sign record should contain information such as:

```text
Sign ID
Gloss
Display Name
Meaning
Category
Subcategory
Aliases
Context
Regional Variant
Source
Recognition Status
Animation Status
Fallback
```

Example:

```json
{
  "id": "isl_000001",
  "gloss": "HELLO",
  "displayName": "Hello",
  "meaning": "Greeting",
  "category": "Everyday",
  "aliases": ["hi", "hey"],
  "recognition": {
    "available": false
  },
  "animation": {
    "available": false
  },
  "fallback": "fingerspell"
}
```

---

# 🤖 AI Architecture

The target AI architecture is:

```text
User Input
    ↓
Language Detection
    ↓
Speech-to-Text (when applicable)
    ↓
Semantic Understanding
    ↓
Intent Detection
    ↓
ISL Gloss Generation
    ↓
Sign Registry
    ↓
Avatar / Response
```

For contextual conversation:

```text
Recognized Sign
+
Conversation Context
+
Pending Question
+
Current Topic
        ↓
AI Response
        ↓
Text / Voice / ISL Response
```

---

# 🧠 Recognition Model Roadmap

The intended hands-only recognition architecture is temporal.

```text
Video Frames
     ↓
Hand Landmarks
     ↓
Feature Extraction
     ↓
Temporal Frame Buffer
     ↓
LSTM / GRU / Temporal Model
     ↓
Sign Classification
     ↓
Confidence
     ↓
Stable Prediction
```

The recognition model will be developed incrementally:

```text
25 signs
   ↓
50 signs
   ↓
100 signs
   ↓
250 signs
   ↓
500+ signs
```

The project should report actual evaluation metrics rather than fabricated accuracy.

Relevant metrics include:

* Accuracy
* Precision
* Recall
* Macro F1
* Confusion Matrix
* Per-class performance

---

# 👋 Sign-to-Response Example

Example:

```text
USER:

🤟 HI

        ↓

HAND RECOGNITION

        ↓

HELLO

        ↓

CONTEXT / INTENT

GREETING

        ↓

SIGNBRIDGE RESPONSE

"Hello! What's up?"

        ↓

OPTIONAL

🔊 Voice

        ↓

OPTIONAL

🤟 3D Avatar Response
```

---

# 🏥 Emergency Communication

A future accessibility mode includes high-priority phrases such as:

```text
I NEED HELP

I NEED A DOCTOR

CALL AN AMBULANCE

I NEED MEDICINE

I NEED DIRECTIONS

I AM IN DANGER
```

Emergency actions should remain clearly separated from ordinary conversational responses.

The application must not trigger external emergency services automatically unless a real, authorized integration exists.

---

# 🎓 Learn ISL

The planned learning module will allow users to:

* Learn signs
* Watch the 3D avatar
* Practice gestures
* Track learning progress
* Build streaks
* Track completed signs
* Review previous practice

Example:

```text
TODAY'S SIGN

HELLO

[ Watch ]

[ Practice ]

Progress:
4 / 5
```

---

# 📊 Translation History

Users can store translation activity such as:

```text
Input:
"Where is the hospital?"

Language:
English

ISL:
ME → HOSPITAL → WHERE

Intent:
Location question

Confidence:
Actual model/system value
```

Future production storage will use the database instead of temporary in-memory history.

---

# ⭐ Saved Phrases

Users will be able to save commonly used phrases.

Examples:

```text
⭐ Hi

⭐ Where is the hospital?

⭐ I need help

⭐ Thank you

⭐ I need water
```

Saved phrases can be replayed through the avatar where genuine animation assets exist.

---

# 🌐 Supported Architecture

## Current / Prototype Components

The current project contains:

* Python
* Streamlit
* React
* Vite
* Three.js
* Node.js
* Express
* CSV-based sign data
* Whisper
* SpeechRecognition
* SoundFile
* Pandas
* NumPy

The repository also contains a React/Vite application configuration and an Express API server.

---

# 🚀 Target Assignment Stack

The production/assignment version is intended to use:

## Frontend

* React.js
* Vite
* React Router
* Tailwind CSS
* Axios
* Three.js

## Backend

* Node.js
* Express.js
* JWT authentication
* bcrypt
* Zod validation

## Database

* Supabase PostgreSQL

## Artificial Intelligence

* Google Gemini API
* Speech-to-Text where required
* Text-to-Speech where required
* Translation services where required

## Deployment

* Vercel — Frontend
* Render — Backend
* Supabase — Database

---

# 🔐 Security

AI credentials and other secrets must remain on the backend.

Never expose:

```text
GEMINI_API_KEY
JWT_SECRET
SUPABASE_SERVICE_ROLE_KEY
```

inside frontend code.

Use environment variables.

Example:

```env
GEMINI_API_KEY=
SUPABASE_URL=
SUPABASE_SERVICE_ROLE_KEY=
JWT_SECRET=
FRONTEND_URL=
PORT=
```

For the React frontend:

```env
VITE_API_BASE_URL=
```

Do not commit real secrets to GitHub.

---

# 📁 Project Structure

Target architecture:

```text
signbridge-ai/
│
├── src/
│   ├── components/
│   │   ├── avatar/
│   │   ├── translator/
│   │   ├── conversation/
│   │   ├── signvision/
│   │   └── common/
│   │
│   ├── pages/
│   │   ├── Login/
│   │   ├── Register/
│   │   ├── Dashboard/
│   │   ├── Translator/
│   │   ├── LiveConversation/
│   │   ├── SignVision/
│   │   ├── LearnISL/
│   │   ├── SignLibrary/
│   │   ├── History/
│   │   ├── SavedPhrases/
│   │   └── Settings/
│   │
│   ├── services/
│   ├── hooks/
│   ├── context/
│   ├── types/
│   └── main.tsx
│
├── server/
│   ├── server.js
│   ├── routes/
│   ├── controllers/
│   ├── services/
│   ├── middleware/
│   ├── validators/
│   └── db/
│
├── public/
│   └── models/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── training/
│   ├── collect_dataset.py
│   ├── extract_hand_landmarks.py
│   ├── prepare_hand_sequences.py
│   ├── train_hand_sign_model.py
│   └── evaluate_hand_sign_model.py
│
├── models/
│
├── supabase/
│   └── migrations/
│
├── docs/
│   ├── API.md
│   └── DEPLOYMENT.md
│
├── app.py
├── package.json
├── package-lock.json
├── vite.config.ts
├── tsconfig.json
├── .env.example
├── .gitignore
└── README.md
```

The exact structure may evolve as the Streamlit prototype is migrated into the required React + Express architecture.

---

# 🛠️ Current Local Setup

## Requirements

Install:

* Node.js
* npm
* Python 3
* pip
* Git

---

# ▶️ Run the Current Streamlit Prototype

Create and activate a Python environment:

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install Python dependencies:

```bash
pip install streamlit openai-whisper SpeechRecognition soundfile numpy pandas deep-translator
```

Run:

```bash
streamlit run app.py
```

The Streamlit application will normally be available at:

```text
http://localhost:8501
```

---

# ▶️ Run the React Frontend

Install dependencies:

```bash
npm install
```

Start Vite:

```bash
npm run dev
```

The project is configured for:

```text
http://localhost:5173
```

---

# ▶️ Run the Express Backend

Start the Node backend:

```bash
npm start
```

or:

```bash
node server.js
```

The current backend uses:

```text
http://localhost:5000
```

---

# 📡 Current API Endpoints

The current Express backend exposes endpoints including:

## Health

```http
GET /api/health
```

## Avatar Configuration

```http
GET /api/avatar-config
```

```http
POST /api/avatar-config
```

## Sign Database

```http
GET /api/signs
```

## Sign Sequence

```http
GET /api/sign-sequence?text=hello
```

## Face Upload

```http
POST /api/upload-face
```

## Apply Face

```http
POST /api/apply-face
```

The production API structure may expand as authentication, AI, database and conversation features are added.

---

# 🔌 Frontend ↔ Backend

During local development, the Vite application uses the Express backend through the `/api` proxy.

Target production architecture:

```text
Vercel
React Frontend
     ↓
HTTPS
     ↓
Render
Express Backend
     ↓
Supabase + Gemini
```

Production code should not depend on:

```text
localhost
127.0.0.1
localhost:5000
```

Instead use environment variables.

---

# 🗄️ Planned Supabase Database

The production database is planned to contain tables such as:

```text
profiles
signs
sign_animations
sign_recognition_classes
translations
conversation_sessions
conversation_messages
saved_phrases
learning_progress
```

---

# 🔑 Authentication Roadmap

The production assignment version will provide:

```http
POST /api/auth/register
POST /api/auth/login
GET /api/auth/me
```

Passwords will be hashed using:

```text
bcrypt
```

Authentication will use:

```text
JWT
```

Protected routes will require a valid token.

---

# 🤖 Gemini Integration

The production backend will use Google Gemini for appropriate AI tasks such as:

* Intent understanding
* Contextual responses
* Semantic normalization
* Conversation assistance
* Response generation

The Gemini API key must exist only on the backend.

Example:

```text
React
  ↓
POST /api/ai/translate
  ↓
Express
  ↓
Gemini
  ↓
Structured result
  ↓
React
```

---

# 🎨 UI/UX Vision

SignBridge is designed around a modern accessibility-first interface.

Design principles:

* Clean light interface
* High readability
* Accessible contrast
* Modern SaaS styling
* Large touch-friendly controls
* Clear status states
* Minimal clutter
* Responsive desktop/mobile layout
* Human-centered interaction
* 3D avatar as a visual focus

Main experience areas:

```text
Dashboard
Translate
Live Conversation
SignVision
Learn ISL
Emergency Assist
History
Saved Phrases
Sign Library
Accessibility
Settings
```

---

# ♿ Accessibility

Accessibility is a core part of the product.

Planned and supported considerations include:

* High contrast
* Large controls
* Readable typography
* Keyboard navigation
* Visible focus states
* Reduced motion
* Captions
* Voice feedback
* Accessible labels
* Responsive layouts

---

# 🧪 Testing Strategy

The project should test multiple layers independently.

## Frontend

* Component testing
* Routing
* API integration
* Responsive layout
* Avatar rendering

## Backend

* Authentication
* Validation
* API endpoints
* Database operations
* Error handling

## AI

* Intent quality
* Semantic mapping
* Contextual responses
* Recognition confidence

## ISL Recognition

* Signer-independent evaluation where possible
* Per-class metrics
* Confusion matrix
* Unknown/uncertain handling

---

# ⚠️ Technical Honesty

SignBridge AI is an evolving research/prototype project.

The project must not claim that:

* every ISL word is recognized
* every sign has a 3D animation
* every sign has perfect recognition
* a hand being detected means a sign was recognized
* 500 signs are fully animated unless 500 genuine assets exist
* a response is fully signed if the required animation assets do not exist

The application should clearly distinguish:

```text
Vocabulary Available
Recognition Available
Animation Available
Fallback Available
```

---

# 🛡️ Privacy

Camera and microphone features should be used only when the user explicitly starts them.

The application should:

* request permissions appropriately
* stop camera streams when no longer required
* stop microphone access after recording
* avoid unnecessary storage of raw recordings
* avoid collecting identity information
* keep API secrets on the server

---

# 📈 Roadmap

## Phase 1 — Core Platform

* [x] Initial SignBridge prototype
* [x] Multilingual input
* [x] Speech processing
* [x] Text input
* [x] ISL meaning layer
* [x] 3D avatar
* [x] Sign sequence concept
* [x] Express backend
* [ ] Production React architecture

## Phase 2 — Communication

* [ ] Context-aware responses
* [ ] Two-way conversation
* [ ] Avatar response signing
* [ ] Conversation history
* [ ] Saved phrases

## Phase 3 — Sign Recognition

* [ ] Real hand landmark detection
* [ ] Hands-only sign recognition
* [ ] Temporal model
* [ ] Confidence handling
* [ ] Unknown-sign detection
* [ ] Continuous sign recognition

## Phase 4 — ISL Knowledge Base

* [ ] Structured sign registry
* [ ] Verified vocabulary
* [ ] 100+ concepts
* [ ] 250+ concepts
* [ ] 500+ concepts

## Phase 5 — Avatar Animation

* [ ] Verified sign-animation mapping
* [ ] Skeleton retargeting
* [ ] Natural hand/finger movement
* [ ] Animation caching
* [ ] Lazy loading
* [ ] 100+ real sign animations
* [ ] 250+ real sign animations
* [ ] 500+ real sign animations

## Phase 6 — Production

* [ ] JWT authentication
* [ ] bcrypt password security
* [ ] Zod validation
* [ ] Supabase PostgreSQL
* [ ] Gemini backend integration
* [ ] Vercel frontend
* [ ] Render backend
* [ ] Production monitoring
* [ ] Security review

---

# 🏗️ Deployment Architecture

The target production architecture is:

```text
                         USERS
                           │
                           ↓
                    ┌─────────────┐
                    │   VERCEL    │
                    │ React/Vite  │
                    │ Tailwind    │
                    │ Three.js    │
                    └──────┬──────┘
                           │
                         HTTPS
                           │
                           ↓
                    ┌─────────────┐
                    │   RENDER    │
                    │ Node/Express│
                    │ JWT / Zod   │
                    └──────┬──────┘
                           │
                ┌──────────┼──────────┐
                ↓          ↓          ↓
           SUPABASE     GEMINI      ISL
           POSTGRES       AI       SERVICES
```

---

# 🌍 Production Environment Variables

## Vercel

```env
VITE_API_BASE_URL=https://your-backend.onrender.com
```

## Render

```env
PORT=
FRONTEND_URL=https://your-app.vercel.app
GEMINI_API_KEY=
SUPABASE_URL=
SUPABASE_SERVICE_ROLE_KEY=
JWT_SECRET=
```

Never commit real environment values.

---

# 🚀 Deployment Plan

## Frontend

Deploy the React/Vite application to:

**Vercel**

Build command:

```bash
npm run build
```

Output:

```text
dist
```

## Backend

Deploy the Express application to:

**Render**

Build:

```bash
npm install
```

Start:

```bash
npm start
```

## Database

Use:

**Supabase PostgreSQL**

## AI

Use:

**Google Gemini API**

---

# 🤝 Contributing

Contributions are welcome.

Recommended workflow:

```bash
git checkout -b feature/your-feature
```

Make changes.

Test locally.

Commit:

```bash
git add .
git commit -m "Add feature"
```

Push:

```bash
git push -u origin feature/your-feature
```

Open a pull request.

---

# 📜 Project Principles

SignBridge AI follows these principles:

### 1. Accessibility First

The product should reduce communication barriers rather than add complexity.

### 2. Human-Centered AI

AI should assist communication naturally, not behave like a rigid command system.

### 3. Technical Honesty

Never fabricate recognition accuracy, sign support or animation availability.

### 4. Real Sign Data

Vocabulary, recognition data and avatar animation assets should be kept as separate verified layers.

### 5. Scalable Architecture

The system should be able to grow from a prototype into a large ISL communication platform.

---

# 👥 Team

**Project:** SignBridge AI

**Domain:** Artificial Intelligence / Accessibility / Indian Sign Language

**Focus Areas:**

* AI
* Computer Vision
* Natural Language Processing
* Accessibility
* 3D Graphics
* Web Development
* Human-Computer Interaction

---

# 🏷️ Current Project Status

**Status:** Active development / hackathon prototype

Current focus:

```text
Realistic 3D Avatar
        +
Natural Conversation
        +
Hands-Only Sign Recognition
        +
500+ ISL Knowledge Base
        +
Production React / Express Architecture
```

---

# 📌 Final Vision

SignBridge AI aims to become more than a translator.

The long-term experience is:

```text
        USER
         │
         │
   Speech / Text / Sign
         │
         ↓
     SIGNBRIDGE AI
         │
    Understand
         │
      Interpret
         │
      Respond
         │
    ┌────┴─────┐
    ↓          ↓
  Text       Voice
    │
    ↓
3D Human Avatar
    │
    ↓
   ISL
```

### The goal:

> **A communication partner that understands, responds, and signs naturally.**

---

## 📄 License

Add the appropriate project license here based on your team's requirements.

Example:

```text
MIT License
```

Do not use a license that conflicts with the licenses/terms of third-party datasets, models, libraries or sign-language resources used by the project.

---

## 🙏 Acknowledgements

SignBridge AI uses open-source technologies and external resources where applicable.

Relevant technologies include:

* React
* Vite
* Three.js
* Node.js
* Express
* Python
* Streamlit
* Whisper
* Supabase
* Google Gemini
* MediaPipe

Third-party datasets and ISL reference resources should be acknowledged according to their respective terms and licenses.
