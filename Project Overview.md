# 🤖 AI Resume Scanner - Project Overview

## 📋 Table of Contents
1. [Project Introduction](#project-introduction)
2. [Technology Stack](#technology-stack)
3. [System Architecture](#system-architecture)
4. [Main Components](#main-components)
5. [System Flow Diagram](#system-flow-diagram)
6. [How It Works](#how-it-works)
7. [Machine Learning Model](#machine-learning-model)
8. [API Endpoints](#api-endpoints)
9. [Deployment](#deployment)
10. [Features](#features)

---

## 🎯 Project Introduction

**AI Resume Scanner** is an intelligent web application that analyzes resumes using Machine Learning and AI to predict the most suitable job category. The system extracts text from PDF resumes, processes it through a trained ML model, and provides category predictions with confidence scores and skill extraction.

### Key Features
- 📄 PDF Resume Upload & Parsing
- 🤖 ML-Powered Category Prediction
- 🎯 Skill Extraction
- 💬 AI Chatbot for Career Guidance
- 📊 Detailed Analysis Results
- 🌐 Fully Deployed on Cloud

---

## 🛠 Technology Stack

### Frontend Technologies
| Technology | Purpose | Version |
|------------|---------|---------|
| **React** | UI Framework | 18.3.1 |
| **TypeScript** | Type Safety | 5.8.3 |
| **Vite** | Build Tool | 5.4.19 |
| **Tailwind CSS** | Styling | 3.4.17 |
| **shadcn/ui** | UI Components | Latest |
| **React Router** | Routing | 6.30.1 |
| **TanStack Query** | Data Fetching | 5.83.0 |
| **Recharts** | Data Visualization | 2.15.4 |
| **Radix UI** | Accessible Components | Various |

### Backend Technologies
| Technology | Purpose | Version |
|------------|---------|---------|
| **FastAPI** | Web Framework | 0.115.5 |
| **Python** | Programming Language | 3.9 |
| **Uvicorn** | ASGI Server | 0.32.1 |
| **scikit-learn** | ML Library | 1.5.2 |
| **pandas** | Data Processing | 2.2.3 |
| **pdfplumber** | PDF Text Extraction | 0.11.4 |
| **OpenAI API** | Chat Feature | 1.51.2 |
| **Pydantic** | Data Validation | 2.9.2 |

### ML & Data Science
- **TF-IDF Vectorization**: Text feature extraction
- **Logistic Regression**: Classification model
- **Pandas**: Dataset processing
- **NumPy**: Numerical computations
- **Dataset**: 42,000+ labeled resumes

### Deployment
- **Frontend**: Vercel (Static Hosting)
- **Backend**: Railway (Python Hosting)
- **Version Control**: GitHub

---

## 🏗 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         React Frontend (Vercel)                      │   │
│  │  ┌────────────┐  ┌────────────┐  ┌──────────────┐  │   │
│  │  │   Home     │  │   Upload  │  │    Result    │  │   │
│  │  │   Page     │  │   Page    │  │    Page      │  │   │
│  │  └────────────┘  └────────────┘  └──────────────┘  │   │
│  │  ┌────────────────────────────────────────────────┐ │   │
│  │  │         AI Chatbot Component                   │ │   │
│  │  └────────────────────────────────────────────────┘ │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/HTTPS
                         │ REST API
┌────────────────────────▼────────────────────────────────────┐
│                     API LAYER                                │
│  ┌──────────────────────────────────────────────────────┐   │
│  │      FastAPI Backend (Railway)                      │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────┐ │   │
│  │  │   /predict  │  │   /chat      │  │  /health │ │   │
│  │  │   Endpoint  │  │   Endpoint   │  │ Endpoint │ │   │
│  │  └──────────────┘  └──────────────┘  └──────────┘ │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                  PROCESSING LAYER                            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  PDF Text Extraction (pdfplumber)                   │   │
│  └────────────────────────┬─────────────────────────────┘   │
│                           │                                   │
│  ┌────────────────────────▼─────────────────────────────┐   │
│  │  ML Model Prediction (scikit-learn)                  │   │
│  │  ┌──────────────────────────────────────────────┐   │   │
│  │  │  TF-IDF Vectorization                        │   │   │
│  │  │  Logistic Regression Classifier              │   │   │
│  │  │  Trained on 42K+ Resume Dataset             │   │   │
│  │  └──────────────────────────────────────────────┘   │   │
│  └────────────────────────┬─────────────────────────────┘   │
│                           │                                   │
│  ┌────────────────────────▼─────────────────────────────┐   │
│  │  Skill Extraction & Category Matching                │   │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🧩 Main Components

### Frontend Components

#### 1. **Pages** (`src/pages/`)
- **Home.tsx**: Landing page with features and CTA
- **Upload.tsx**: Resume upload interface with drag-and-drop
- **Result.tsx**: Displays analysis results with visualizations
- **About.tsx**: Project information and tech stack
- **NotFound.tsx**: 404 error page

#### 2. **Components** (`src/components/`)
- **Navbar.tsx**: Navigation bar with theme toggle
- **OpenAIChat.tsx**: AI chatbot for career guidance
- **ChatbotIcon.tsx**: Floating chatbot button
- **ui/**: 50+ shadcn/ui components (buttons, cards, dialogs, etc.)

#### 3. **Utilities**
- **utils.ts**: Helper functions and utilities
- **hooks/**: Custom React hooks
- **lib/**: Shared libraries

### Backend Components

#### 1. **API Routes** (`backend/app/main.py`)
- **`/`**: Root endpoint with API information
- **`/health`**: Health check endpoint
- **`/predict`**: Resume analysis endpoint (POST)
- **`/chat`**: AI chatbot endpoint (POST)

#### 2. **Core Functions**
- **`extract_text_from_pdf()`**: Extracts text from PDF files
- **`predict_category()`**: ML model prediction
- **`extract_skills()`**: Extracts skills from resume text
- **`_load_and_train_model()`**: Trains ML model on startup

#### 3. **ML Model**
- **TF-IDF Vectorizer**: Converts text to numerical features
- **Logistic Regression**: Multi-class classifier
- **Dataset**: 42,000+ labeled resumes for training

---

## 🔄 System Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER INTERACTION FLOW                         │
└─────────────────────────────────────────────────────────────────┘

1. USER VISITS FRONTEND (Vercel)
   │
   ├─► Home Page
   │   └─► Learn about features
   │
   ├─► Upload Page
   │   └─► Select/Drag PDF Resume
   │
   └─► [User clicks "Analyze Resume"]
              │
              ▼
┌─────────────────────────────────────────────────────────────┐
│  FRONTEND: Upload.tsx                                        │
│  - Validates PDF file                                        │
│  - Creates FormData                                          │
│  - Sends POST request to /predict                            │
└──────────────────────┬───────────────────────────────────────┘
                      │
                      │ HTTP POST
                      │ /predict
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  BACKEND: FastAPI /predict Endpoint                          │
│                                                              │
│  1. Receives PDF File                                       │
│     │                                                        │
│     ▼                                                        │
│  2. PDF Text Extraction (pdfplumber)                        │
│     │                                                        │
│     ▼                                                        │
│  3. ML Model Prediction                                     │
│     ├─► Check if ML model is trained                        │
│     ├─► If YES: Use ML model (TF-IDF + Logistic Regression) │
│     └─► If NO: Use weighted keyword matching                │
│     │                                                        │
│     ▼                                                        │
│  4. Extract Skills from Text                                │
│     │                                                        │
│     ▼                                                        │
│  5. Return Prediction Response                              │
│     {                                                       │
│       category: "Data Science",                             │
│       confidence: 0.87,                                     │
│       skills: ["Python", "Machine Learning", ...]          │
│     }                                                       │
└──────────────────────┬───────────────────────────────────────┘
                      │
                      │ JSON Response
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  FRONTEND: Result.tsx                                        │
│  - Receives prediction result                               │
│  - Displays category with confidence                        │
│  - Shows extracted skills                                   │
│  - Renders visualizations (charts)                         │
│  - Provides AI chat option                                  │
└─────────────────────────────────────────────────────────────┘
```

### Machine Learning Model Training Flow

```
┌─────────────────────────────────────────────────────────────┐
│  BACKEND STARTUP (on_startup event)                         │
│                                                              │
│  1. Load Environment Variables                              │
│     │                                                        │
│     ▼                                                        │
│  2. Locate Dataset (resume-dataset.csv)                      │
│     - Try multiple paths                                    │
│     - Check ../src/assets/                                  │
│     - Check ./resume-dataset.csv                            │
│     │                                                        │
│     ▼                                                        │
│  3. Load & Preprocess Dataset                               │
│     - Read CSV with pandas                                  │
│     - Clean null values                                     │
│     - Normalize category names                              │
│     - Filter short resumes                                  │
│     │                                                        │
│     ▼                                                        │
│  4. Train ML Model                                          │
│     ├─► TF-IDF Vectorization                               │
│     │   - ngrams: 1-3 words                                 │
│     │   - max_features: 10,000                             │
│     │   - stop_words: English                              │
│     │                                                        │
│     ├─► Logistic Regression                                │
│     │   - solver: 'lbfgs'                                  │
│     │   - multi_class: 'multinomial'                       │
│     │   - max_iter: 2000                                    │
│     │                                                        │
│     └─► Cross-Validation                                   │
│         - 5-fold CV                                         │
│         - Calculate accuracy                                │
│     │                                                        │
│     ▼                                                        │
│  5. Store Model in Memory                                   │
│     - _ml_pipeline: Trained model                          │
│     - _ml_label_list: Category labels                      │
│     │                                                        │
│     ▼                                                        │
│  6. Log Training Results                                    │
│     - Number of samples                                     │
│     - Categories found                                      │
│     - Cross-validation accuracy                             │
└─────────────────────────────────────────────────────────────┘
```

---

## ⚙️ How It Works

### Step-by-Step Process

#### 1. **User Uploads Resume**
- User visits the web application
- Navigates to Upload page
- Selects or drags-and-drops a PDF resume file
- Clicks "Analyze Resume" button

#### 2. **Frontend Processing**
- Validates file type (must be PDF)
- Creates FormData object with the file
- Sends POST request to backend API endpoint
- Shows loading state during processing

#### 3. **Backend Processing**
```python
# Pseudo-code flow
1. Receive PDF file via FastAPI endpoint
2. Extract text using pdfplumber:
   - Open PDF in memory (io.BytesIO)
   - Iterate through pages
   - Extract text from each page
   - Combine into single string
3. Predict category using ML model:
   - If ML model is trained:
     - Vectorize text (TF-IDF)
     - Predict category probabilities
     - Select highest probability category
   - Else (fallback):
     - Use weighted keyword matching
     - Score each category
     - Select highest scoring category
4. Extract skills:
   - Match keywords from resume text
   - Use word boundaries for accuracy
   - Return top skills found
5. Return JSON response:
   {
     "category": "Data Science",
     "confidence": 0.87,
     "skills": ["Python", "Machine Learning", ...]
   }
```

#### 4. **Result Display**
- Frontend receives prediction result
- Displays category with confidence percentage
- Shows extracted skills as badges
- Renders charts/graphs for visualization
- Provides option to chat with AI for career advice

#### 5. **AI Chat Feature** (Optional)
- User can click chatbot icon
- Enter OpenAI API key (or use server-side key)
- Ask questions about career/resume
- Get AI-powered responses

---

## 🤖 Machine Learning Model

### Model Architecture

```
INPUT: Resume Text (String)
    │
    ▼
┌─────────────────────────────────────┐
│  TEXT PREPROCESSING                 │
│  - Lowercase conversion             │
│  - Remove special characters        │
│  - Tokenization                     │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  TF-IDF VECTORIZATION               │
│  - n-gram range: (1, 3)            │
│  - Max features: 10,000             │
│  - Stop words: English              │
│  - Output: Numerical feature vector │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  LOGISTIC REGRESSION CLASSIFIER      │
│  - Multi-class classification       │
│  - Solver: L-BFGS                   │
│  - Regularization: C=1.0            │
│  - Output: Category probabilities   │
└──────────────┬──────────────────────┘
               │
               ▼
OUTPUT: Category + Confidence Score
```

### Training Data
- **Dataset Size**: 42,000+ labeled resumes
- **Categories**: 7 job categories
  - Data Science
  - Software Engineering
  - DevOps / Cloud
  - Product Management
  - UI/UX Design
  - Data Engineering
  - Cybersecurity
- **Features**: Resume text content
- **Labels**: Job category

### Model Performance
- **Training Method**: Supervised Learning
- **Validation**: 5-fold Cross-Validation
- **Evaluation Metric**: Accuracy
- **Expected Accuracy**: 70-85% (varies by dataset)

### Prediction Process
1. **Text Extraction**: PDF → Plain Text
2. **Feature Extraction**: Text → TF-IDF Vectors
3. **Classification**: Vectors → Category Probabilities
4. **Selection**: Highest probability → Predicted Category
5. **Skill Extraction**: Pattern matching for skills

---

## 🔌 API Endpoints

### Base URL
```
Production: https://ai-resume-scanner-backend-production.up.railway.app
```

### Endpoints

#### 1. **GET /** - API Information
```http
GET /
```
**Response:**
```json
{
  "status": "ok",
  "message": "AI Resume Scanner API",
  "version": "1.0.0",
  "endpoints": {
    "health": "/health",
    "predict": "/predict",
    "chat": "/chat"
  }
}
```

#### 2. **GET /health** - Health Check
```http
GET /health
```
**Response:**
```json
{
  "status": "ok"
}
```

#### 3. **POST /predict** - Resume Analysis
```http
POST /predict
Content-Type: multipart/form-data
```
**Request:**
- `file`: PDF file (multipart/form-data)

**Response:**
```json
{
  "category": "Data Science",
  "confidence": 0.87,
  "skills": [
    "Python",
    "Machine Learning",
    "Pandas",
    "Numpy"
  ]
}
```

#### 4. **POST /chat** - AI Chatbot
```http
POST /chat
Content-Type: application/json
X-OpenAI-Api-Key: <optional-api-key>
```
**Request:**
```json
{
  "messages": [
    {
      "role": "user",
      "content": "How can I improve my resume?"
    }
  ],
  "model": "gpt-4o-mini"
}
```
**Response:**
```json
{
  "content": "Here are some tips to improve your resume..."
}
```

---

## 🚀 Deployment

### Frontend Deployment (Vercel)
1. **Platform**: Vercel
2. **Framework**: Vite + React
3. **Build Command**: `npm run build`
4. **Output Directory**: `dist`
5. **Environment Variables**:
   - `VITE_BACKEND_URL`: Backend API URL

### Backend Deployment (Railway)
1. **Platform**: Railway
2. **Runtime**: Python 3.9
3. **Framework**: FastAPI + Uvicorn
4. **Build**: Nixpacks (auto-detected)
5. **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. **Environment Variables**:
   - `PORT`: Auto-set by Railway
   - `OPENAI_API_KEY`: Optional (for chat feature)

### Deployment Architecture
```
┌─────────────────────────────────────────┐
│         Internet/Users                   │
└──────────────┬──────────────────────────┘
               │
               │ HTTPS
               │
    ┌──────────▼──────────┐
    │   Vercel (Frontend) │
    │  React Application  │
    └──────────┬──────────┘
               │
               │ API Calls
               │
    ┌──────────▼──────────┐
    │ Railway (Backend)   │
    │  FastAPI Server     │
    │  + ML Model         │
    └─────────────────────┘
```

---

## ✨ Features

### Core Features
1. ✅ **PDF Resume Upload**
   - Drag-and-drop interface
   - File validation
   - Progress indication

2. ✅ **ML-Powered Prediction**
   - Trained on 42K+ resumes
   - 7 job categories
   - Confidence scores

3. ✅ **Skill Extraction**
   - Automatic skill detection
   - Weighted keyword matching
   - Visual display

4. ✅ **AI Chatbot**
   - Career guidance
   - Resume improvement tips
   - OpenAI GPT integration

5. ✅ **Results Visualization**
   - Category display
   - Confidence visualization
   - Skills badges
   - Charts and graphs

6. ✅ **Responsive Design**
   - Mobile-friendly
   - Dark/Light theme
   - Modern UI/UX

### Technical Features
- Type-safe codebase (TypeScript)
- RESTful API architecture
- CORS enabled
- Error handling
- Loading states
- Toast notifications
- Health monitoring

---

## 📊 Project Statistics

- **Frontend LOC**: ~5,000+ lines
- **Backend LOC**: ~350 lines
- **Components**: 50+ UI components
- **API Endpoints**: 4
- **ML Model**: Trained on 42K+ samples
- **Categories**: 7 job categories
- **Dataset Size**: 3.1 MB CSV

---

## 🔐 Security Features

- API key stored server-side (optional)
- Input validation (file type, size)
- CORS configuration
- Error handling (no sensitive data exposure)
- Environment variables for secrets

---

## 📈 Future Enhancements

- [ ] Multi-language support
- [ ] Additional job categories
- [ ] Resume scoring/ranking
- [ ] Job matching algorithm
- [ ] Export analysis as PDF
- [ ] User accounts and history
- [ ] Advanced ML models (Neural Networks)
- [ ] Real-time collaboration

---

## 📝 License

This project is open source and available for educational purposes.

---

## 👥 Credits

**Project**: AI Resume Scanner  
**Technology**: React, TypeScript, FastAPI, Python, scikit-learn  
**Deployment**: Vercel + Railway  
**Dataset**: 42,000+ labeled resumes

---

*Last Updated: 2025*

