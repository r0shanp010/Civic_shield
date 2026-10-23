# 🛡️ CivicShield — Web Application Deployment & Architecture Guide

This document provides complete instructions for running, hosting, containerizing, and presenting **CivicShield** as a production-grade Web Application.

---

## 🏗️ 1. Web Application System Architecture

CivicShield is built on a **Decoupled Single-Page Application (SPA) Client-Server Architecture**:

```
[ Browser / Mobile Client ]
         │
         ▼  (HTTPS / REST / JWT)
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND (React 18 + Vite)                   │
│   • Responsive Glassmorphism UI & Dashboard Metrics            │
│   • 12-Character Strong Password Suggestion Engine              │
│   • Real-Time Progress Bar (% Done) Case Tracker                │
│   • HTML5 AI Voice Synthesis Assistant                          │
└─────────────────────────────────────────────────────────────────┘
         │
         ▼  (JSON API Endpoints / multipart/form-data)
┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND (FastAPI + Uvicorn)                  │
│   • Role-Based Access Control (Admin / Officer / Citizen)       │
│   • JWT Auth Bearer Tokens & Argon2/Bcrypt Password Hashing     │
│   • Evidence File Upload & Serving Gateway                      │
└─────────────────────────────────────────────────────────────────┘
         │
         ├──► [ Scikit-Learn NLP Machine Learning Pipeline ]
         │      - TF-IDF Vectorizer
         │      - Logistic Regression (Category Classifier)
         │      - Department Recommender & Priority Decision Matrix
         │      - Duplicate Cosine Similarity Engine
         │
         └──► [ Database Layer (SQLite / MySQL / PostgreSQL) ]
                - Complaints, Timeline Updates, Admin Users, Predictions
```

---

## 🚀 2. Three Ways to Run & Deploy the Web Application

### Option A: Instant 1-Click Launchers (Local & Network)

| Launcher Script | What It Does | Best Used For |
| :--- | :--- | :--- |
| **`start_web_app.bat`** | Starts backend (`8000`), starts frontend (`5173`), and opens browser automatically | Day-to-day development & testing |
| **`start_network_share.bat`** | Hosts across Wi-Fi so phones & other laptops can connect via `http://<YOUR_IP>:5173` | Showing to faculty on their phones |
| **`start_public_tunnel.bat`** | Generates an instant public HTTPS link (`https://...loca.lt`) over the internet | Live online demo with no cloud setup |

---

### Option B: Docker & Docker Compose (Containerized Production)

CivicShield includes full production `Dockerfile`s and `docker-compose.yml`:

1. Open a terminal in the project directory:
   ```bash
   docker-compose up --build
   ```
2. Open your browser:
   - **Web App:** `http://localhost` or `http://localhost:5173`
   - **Backend API Docs:** `http://localhost:8000/docs`

---

### Option C: 100% Free Cloud Deployment (Vercel + Render)

#### 1. Push to GitHub:
```bash
git init
git add .
git commit -m "CivicShield Web Application"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/civicshield.git
git push -u origin main
```

#### 2. Deploy Backend on [Render.com](https://render.com) (Free):
- Click **New +** $\rightarrow$ **Web Service** $\rightarrow$ Connect GitHub Repo.
- **Root Directory:** `backend`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Render generates your backend URL: e.g. `https://civicshield-backend.onrender.com`

#### 3. Deploy Frontend on [Vercel.com](https://vercel.com) (Free):
- Click **Add New...** $\rightarrow$ **Project** $\rightarrow$ Connect GitHub Repo.
- **Root Directory:** `frontend`
- **Build Command:** `npm run build`
- **Output Directory:** `dist`
- **Environment Variable:** `VITE_API_URL` = `https://civicshield-backend.onrender.com`
- Vercel generates your live web address: e.g. `https://civicshield.vercel.app`

---

## 📋 3. Faculty / Review 1 Viva Cheat-Sheet

When presenting CivicShield to your guide/faculty, explain the 4 layers:

1. **Client Tier:** React 18 SPA utilizing Vite bundler, Lucide icons, responsive CSS variables, and HTML5 Web Speech API for voice briefings.
2. **Security Tier:** 12-character high-entropy password generation algorithm (Fisher-Yates shuffle), JWT Bearer authentication, and SHA-256 / Bcrypt password hashing.
3. **AI / ML Tier:** Natural Language Processing (NLP) pipeline combining TF-IDF vectorization with multi-class Logistic Regression for category classification, Cosine Similarity for duplicate complaint detection, and a heuristic priority decision matrix based on monetary amount and severity.
4. **Data & Storage Tier:** Relational SQL database schema with automated foreign keys, cascade status tracking, and evidence file attachments.
