# 🔎 TruthLens

### Explainable AI for Document Verification and Evidence-Based Investigation

TruthLens is an AI-powered document investigation platform that helps users analyze information scattered across multiple documents.

Instead of simply generating an answer, TruthLens breaks an investigation into smaller steps: extracting claims, identifying supporting evidence, detecting contradictions, calculating confidence, and presenting the reasoning behind the result.

> **Help users understand not only what information was found, but why it can or cannot be trusted.**

---

## 🚀 Why TruthLens?

Important information is often distributed across reports, PDFs, records, statements, and other documents.

Manually verifying this information can require users to:

- Read multiple documents
- Find important claims
- Locate supporting evidence
- Compare statements
- Detect contradictions
- Determine which information is more reliable
- Keep track of previous investigations

This process is slow, difficult to scale, and prone to human error.

**TruthLens brings these steps into one evidence-aware investigation workflow.**

---

## ✨ Core Features

### 📄 Document Processing

Upload and process documents for investigation.

- PDF document support
- Text extraction
- Document metadata
- Page-level information
- Document library
- Processing status

### 🧩 Claim Extraction

Identify meaningful claims from processed documents.

Claims can be connected to their source documents and supporting context, making it easier to trace information back to its origin.

### 🔍 Evidence Analysis

Trace claims back to the evidence from which they were derived.

TruthLens keeps investigations grounded in document content rather than presenting unsupported conclusions.

### ⚠️ Conflict Detection

Compare information across documents and identify potentially conflicting claims.

Example:

```text
Document A
"Project completion date: March 2025"

Document B
"Project completion date: June 2025"

            ↓

Potential Conflict Detected
```

### 📊 Confidence Scoring

TruthLens provides confidence information to help users understand how strongly the available evidence supports an investigation finding.

Confidence is intended as an aid to decision-making, not as a replacement for human judgment.

### 🧠 Explainable Investigation

Investigation results are presented through relationships between:

```text
Documents
    ↓
Claims
    ↓
Evidence
    ↓
Conflicts
    ↓
Confidence
    ↓
Investigation Result
```

This makes the investigation process easier to inspect and understand.

### 📈 Investigation Dashboard

The interactive dashboard provides access to:

- Investigation history
- Claims
- Evidence
- Conflicts
- Confidence information
- Investigation graphs
- Claim relationships
- Document library

### 🕒 Temporal Claim Tracking

Claims can contain temporal information such as:

- Effective date
- Version
- Source document

This helps distinguish information that may have changed over time.

---

# 🤖 Investigation Workflow

TruthLens follows an evidence-aware investigation pipeline.

```text
                    User Question
                         │
                         ▼
                 Document Collection
                         │
                         ▼
                 Document Processing
                         │
                         ▼
                   Claim Extraction
                         │
                         ▼
                  Evidence Analysis
                         │
                         ▼
                 Conflict Detection
                         │
                         ▼
                 Confidence Analysis
                         │
                         ▼
                Explainable Findings
                         │
                         ▼
                    Human Review
```

The system is designed around a **human-in-the-loop** approach.

TruthLens assists with investigation and analysis while keeping the final interpretation with the user.

---

# 🏗️ System Architecture

```text
┌──────────────────────────────────────────────┐
│                  FRONTEND                    │
│              Next.js + TypeScript            │
│                                              │
│ Dashboard │ Claims │ Evidence │ Graph       │
│ History   │ Library │ Investigations         │
└──────────────────────┬───────────────────────┘
                       │
                       │ REST API
                       ▼
┌──────────────────────────────────────────────┐
│                  BACKEND                     │
│                   FastAPI                    │
│                                              │
│ Document Processing                          │
│ Claim Analysis                               │
│ Evidence Analysis                            │
│ Conflict Detection                           │
│ Confidence Analysis                          │
│ Investigation Management                     │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│                 DATA LAYER                   │
│          PostgreSQL + SQLAlchemy              │
│                                              │
│ Documents │ Chunks │ Claims │ Evidence       │
│ Conflicts │ Investigations │ Analytics       │
└──────────────────────────────────────────────┘
```

---

# 🛠️ Technology Stack

## Frontend

- Next.js
- React
- TypeScript
- HTML/CSS

## Backend

- Python
- FastAPI
- REST APIs
- Pydantic

## Database

- PostgreSQL
- SQLAlchemy

## Document Processing

- PyMuPDF
- pypdf
- Python-based document processing

## OCR

- Tesseract OCR
- pytesseract
- Pillow

## Reporting

- ReportLab

## Development & Deployment

- Git
- GitHub
- Vercel
- Render

---

# 📁 Project Structure

```text
TruthLens/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── claims/
│   │   │   ├── conflicts/
│   │   │   ├── confidence/
│   │   │   ├── documents/
│   │   │   ├── evidence/
│   │   │   ├── investigations/
│   │   │   └── search/
│   │   │
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   └── main.py
│   │
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── app/
│   ├── components/
│   ├── lib/
│   └── package.json
│
└── README.md
```

---

# ⚙️ Local Setup

## 1. Clone the Repository

```bash
git clone https://github.com/Muskankr/Truthlens.git
cd Truthlens
```

---

## 2. Backend Setup

Navigate to the backend:

```bash
cd backend
```

Create a virtual environment.

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 3. Configure Environment Variables

Create:

```text
backend/.env
```

Add your PostgreSQL connection string:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/truthlens
```

Do not commit `.env` files or database credentials to GitHub.

---

## 4. Initialize the Database

Run:

```bash
python -m app.db.init_db
```

This initializes the database tables required by the application.

---

## 5. Start the Backend

From the `backend` directory:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 💻 Frontend Setup

Open another terminal:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Create:

```text
frontend/.env.local
```

Add:

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000/api
```

Start the development server:

```bash
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:3000
```

---

# 🔐 Security & Responsible AI

TruthLens is designed as an **evidence-assistance system**, not an unquestionable source of truth.

Important principles include:

- Evidence should remain traceable to source documents.
- Confidence scores should not be treated as absolute certainty.
- Conflicting information should be surfaced rather than silently ignored.
- Users should be able to inspect the reasoning behind findings.
- Sensitive documents should be handled responsibly.
- Human review remains important for high-impact decisions.

---

# 🎯 Example Use Cases

## Research

Compare information across multiple reports or research documents.

## Compliance

Identify inconsistencies between policies, records, and supporting documents.

## Journalism & Fact Verification

Trace claims to documentary evidence and identify conflicting statements.

## Legal & Administrative Research

Organize information across large collections of records for human review.

## Business Intelligence

Compare reports and identify inconsistencies in organizational information.

## Knowledge Management

Build searchable relationships between documents, claims, and evidence.

---

# 🌟 What Makes TruthLens Different?

Traditional document tools generally focus on:

> **"Find information."**

TruthLens focuses on:

> **"Investigate information."**

The system connects:

```text
Documents
    ↓
Claims
    ↓
Evidence
    ↓
Conflicts
    ↓
Confidence
    ↓
Findings
```

This creates an investigation-oriented workflow rather than a simple document search experience.

---

---

# 📌 Project Status

TruthLens is an actively developed prototype focused on explainable, evidence-aware document investigation.

The architecture is designed to support additional investigation capabilities as the system evolves.

---

# 👩‍💻 Author

**Muskan Kumari**

B.Tech CSE (AI & ML)

GitHub: https://github.com/Muskankr

---

# 📜 License

This project is intended for educational, research, and prototype development purposes.

See the repository for licensing details.
