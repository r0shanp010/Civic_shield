# CivicShield – AI-Based Anonymous Corruption & Bribery Complaint Management System

CivicShield is a secure, anonymous web platform designed for citizens to report suspected corruption, bribery, misuse of authority, and related misconduct without exposing their identities. It features an advanced administrative workstation where officers can review AI-assisted classifications, department recommendations, priority ratings, duplicate warnings, and suspicion flags, and then manage the complaint lifecycle.

---

## 🏛️ System Features
- **Citizen Portal**: File anonymous complaints, upload evidence documents (PDF, JPG, PNG, DOCX), receive a secure tracking key, and view a public investigation timeline.
- **Admin Workstation**: Secure JWT login, stats dashboards, advanced sorting/filters/search filters, AI prediction evaluations, manual investigation history updates, and auto-routing assignments.
- **AI Analytics Services**: Classifies complaints into categories, recommends target departments, grades priority tiers, computes similarity match ratios to flag duplicates, and triggers flags on suspicious repetitiveness.

---

## 🛠️ Project Structure
```text
civicshield/
├── backend/
│   ├── app/
│   │   ├── ai/
│   │   │   ├── preprocessing.py         # NLP text cleanups
│   │   │   ├── classifier.py            # AI prediction & similarity check engine
│   │   │   └── train_models.py          # Synthetic dataset model training
│   │   ├── models/
│   │   │   └── models.py                # SQLAlchemy database models
│   │   ├── routes/
│   │   │   ├── auth.py                  # JWT authentication routes
│   │   │   ├── complaints.py            # Whistleblower reporting routes
│   │   │   └── admin.py                 # Case triage & dashboard routes
│   │   ├── schemas/
│   │   │   └── schemas.py               # Pydantic data validators
│   │   ├── utils/
│   │   │   └── auth.py                  # Password hash & token helpers
│   │   ├── config.py                    # Environment settings
│   │   ├── database.py                  # SQLAlchemy session manager
│   │   └── main.py                      # FastAPI root execution
│   ├── .env                             # Active configs
│   ├── .env.example                     # Sample configs
│   └── requirements.txt                 # Backend requirements
└── frontend/
    ├── src/
    │   ├── pages/
    │   │   ├── Home.jsx                 # Whistleblower Landing Portal
    │   │   ├── SubmitComplaint.jsx      # Multi-section filing form
    │   │   ├── TrackComplaint.jsx       # Public tracking timeline
    │   │   ├── AdminLogin.jsx           # Secure officer login
    │   │   ├── AdminDashboard.jsx       # Metrics & queries panel
    │   │   └── ComplaintDetail.jsx      # Case files & triage control
    │   ├── App.jsx                      # Routing structure
    │   ├── index.css                    # Visual styling variables
    │   └── main.jsx                     # Entry mount
    ├── index.html                       # Base HTML file
    ├── package.json                     # Frontend requirements
    └── vite.config.js                   # Vite configuration
```

---

## 🚀 Installation & Running

### Prerequisites
- Python 3.10+
- Node.js v18+ & npm

---

### 1. Backend Setup (FastAPI)
1. Open a terminal and navigate to the `backend` folder:
   ```bash
   cd backend
   ```
2. Install Python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the backend server:
   ```bash
   python -m uvicorn app.main:app --reload
   ```
   The backend will run on **`http://localhost:8000`**. On startup, it automatically creates the SQLite database `civicshield.db` in the backend folder and seeds default admin accounts.
   - **Interactive Swagger Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)

#### 🤖 (Optional) Train the AI Models
To activate trained scikit-learn models (instead of the smart keyword-heuristics fallback), install `scikit-learn` and run:
```bash
python app/ai/train_models.py
```
This trains Logistic Regression models on a synthetic complaint dataset and saves the pickled models in `backend/app/ai/models/`. If not run, the backend runs gracefully using the built-in regex keywords classifier.

---

### 2. Frontend Setup (React + Vite)
1. Open a new terminal and navigate to the `frontend` folder:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```
   The frontend will run on **`http://localhost:5173`**. Open this URL in your web browser.

---

## 🔑 Seeding / Testing Credentials
To access the admin workbench, navigate to **`http://localhost:5173/admin/login`** and use:
- **Username**: `admin`
- **Password**: `admin123`
*Or (Investigator role)*:
- **Username**: `officer1`
- **Password**: `officer123`

---

## 🛡️ Security and Privacy Design
1. **Zero-Personal Information**: Citizens are warned never to type names, IDs, or phone numbers.
2. **Secure Passwords**: Passwords hashed using standard `bcrypt`.
3. **Session Protection**: All `/api/admin/*` endpoints are protected by OAuth2 JWT Bearer tokens.
4. **Validation**: Enforces strict file extension check (PDF, JPG, PNG, DOCX) and size cap (10MB) for evidence attachments.
5. **No Automated Decisions**: AI scores only guide officials. Final status changes and assignments are made exclusively by authorized personnel.
