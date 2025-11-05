from fastapi import FastAPI, UploadFile, File, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import io
import os
from typing import List, Tuple, Optional

try:
    import pdfplumber  # type: ignore
except Exception as exc:  # pragma: no cover
    pdfplumber = None  # fallback handled below

# ML imports (optional if dataset available)
try:
    import pandas as pd  # type: ignore
    from sklearn.feature_extraction.text import TfidfVectorizer  # type: ignore
    from sklearn.linear_model import LogisticRegression  # type: ignore
    from sklearn.pipeline import Pipeline  # type: ignore
    from sklearn.model_selection import train_test_split  # type: ignore
    from sklearn.metrics import accuracy_score  # type: ignore
except Exception:  # pragma: no cover
    pd = None
    TfidfVectorizer = None
    LogisticRegression = None
    Pipeline = None
    train_test_split = None
    accuracy_score = None

# OpenAI (server-side chat)
try:
    from openai import OpenAI  # type: ignore
except Exception:
    OpenAI = None
try:
    from dotenv import load_dotenv  # type: ignore
except Exception:
    load_dotenv = None


class PredictionResponse(BaseModel):
    category: str
    confidence: float
    skills: List[str]


app = FastAPI(title="Resume Job Predictor", version="1.0.0")

# Allow Vite dev server and common local origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins to support file:// and unknown dev hosts
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def extract_text_from_pdf(file_bytes: bytes) -> str:
    if not pdfplumber:
        raise HTTPException(status_code=500, detail="PDF parser not available")
    text_parts: List[str] = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            if page_text:
                text_parts.append(page_text)
    return "\n".join(text_parts)


JobCategory = Tuple[str, List[str]]

CATEGORIES: List[JobCategory] = [
    ("Data Science", ["python", "pandas", "numpy", "machine learning", "statistics", "sql", "scikit", "tensorflow", "pytorch", "data analysis"]),
    ("Software Engineering", ["javascript", "typescript", "react", "node", "java", "c++", "c#", "go", "docker", "kubernetes", "git", "api", "microservices"]),
    ("DevOps / Cloud", ["aws", "azure", "gcp", "terraform", "ansible", "ci/cd", "jenkins", "kubernetes", "docker", "linux", "sre"]),
    ("Product Management", ["product", "roadmap", "stakeholder", "metrics", "kpi", "user research", "backlog", "agile", "scrum"]),
    ("UI/UX Design", ["figma", "sketch", "wireframe", "prototype", "ux", "ui", "usability", "design system", "adobe"]),
    ("Data Engineering", ["spark", "airflow", "kafka", "hadoop", "etl", "data pipeline", "snowflake", "redshift", "databricks"]),
    ("Cybersecurity", ["security", "siem", "soc", "incident response", "vulnerability", "nist", "owasp", "splunk", "iso 27001"]),
]


def predict_category(text: str) -> PredictionResponse:
    """Predict category using ML model if available; fallback to heuristic keywords."""
    # Try ML model first
    if _ml_pipeline is not None and _ml_label_list is not None:
        try:
            proba = _ml_pipeline.predict_proba([text])[0]
            top_idx = int(proba.argmax())
            category = _ml_label_list[top_idx]
            confidence = float(proba[top_idx])
            # Extract skills via heuristic regardless
            skills_display = extract_skills(text)
            return PredictionResponse(category=category, confidence=round(confidence, 2), skills=skills_display)
        except Exception:
            # fall through to heuristic
            pass

    # Heuristic fallback
    text_lower = text.lower()
    best_category = "General"
    best_score = 0
    best_skills: List[str] = []

    for category, keywords in CATEGORIES:
        score = 0
        matched: List[str] = []
        for kw in keywords:
            if kw in text_lower:
                score += 1
                matched.append(kw)
        if score > best_score:
            best_score = score
            best_category = category
            best_skills = matched

    confidence = min(0.95, 0.5 + (best_score / 10.0)) if best_score > 0 else 0.5
    skills_display = [s.title() for s in best_skills][:10] or ["Communication", "Teamwork"]

    return PredictionResponse(category=best_category, confidence=round(confidence, 2), skills=skills_display)


def extract_skills(text: str) -> List[str]:
    text_lower = text.lower()
    matched: List[str] = []
    for _, keywords in CATEGORIES:
        for kw in keywords:
            if kw in text_lower and kw not in matched:
                matched.append(kw)
    display = [s.title() for s in matched][:10]
    return display if display else ["Communication", "Teamwork"]


@app.get("/")
def root() -> dict:
    return {
        "status": "ok",
        "message": "AI Resume Scanner API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "predict": "/predict",
            "chat": "/chat"
        }
    }


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
async def predict(file: UploadFile = File(...)) -> PredictionResponse:
    if file.content_type not in ("application/pdf", "application/octet-stream"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    file_bytes = await file.read()
    if len(file_bytes) == 0:
        raise HTTPException(status_code=400, detail="Empty file")

    try:
        text = extract_text_from_pdf(file_bytes)
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail=f"Failed to parse PDF: {exc}")

    return predict_category(text)


# --- ML model training on startup (optional) ---
_ml_pipeline: Optional[Pipeline] = None
_ml_label_list: Optional[List[str]] = None


def _load_and_train_model() -> None:
    global _ml_pipeline, _ml_label_list

    if not (pd and TfidfVectorizer and LogisticRegression and Pipeline):
        return  # sklearn/pandas missing

    # Resolve dataset path relative to backend dir
    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dataset_path = os.path.normpath(os.path.join(backend_dir, "../src/assets/resume-dataset.csv"))
    if not os.path.exists(dataset_path):
        return

    try:
        df = pd.read_csv(dataset_path)
        if "Category" not in df.columns or "Resume" not in df.columns:
            return
        # Clean data
        df = df.dropna(subset=["Category", "Resume"]).reset_index(drop=True)
        texts: List[str] = df["Resume"].astype(str).tolist()
        labels: List[str] = df["Category"].astype(str).tolist()

        _ml_label_list = sorted(list(set(labels)))

        pipeline = Pipeline([
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_features=50000)),
            ("clf", LogisticRegression(max_iter=1000, n_jobs=None, verbose=0)),
        ])

        pipeline.fit(texts, labels)
        _ml_pipeline = pipeline
    except Exception:
        # leave model as None on any failure
        _ml_pipeline = None
        _ml_label_list = None


@app.on_event("startup")
def on_startup() -> None:
    # Load .env for server-side secrets
    if load_dotenv:
        try:
            # Load backend/.env
            backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            env_path = os.path.join(backend_dir, ".env")
            if os.path.exists(env_path):
                load_dotenv(env_path)
            else:
                load_dotenv()
        except Exception:
            pass
    _load_and_train_model()


# -------- Server-side Chat with OpenAI (keeps API key private) --------
class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    model: Optional[str] = None


class ChatResponse(BaseModel):
    content: str


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest, x_openai_api_key: Optional[str] = Header(default=None)) -> ChatResponse:
    if OpenAI is None:
        raise HTTPException(status_code=500, detail="OpenAI client not installed on server")
    # Allow per-request override via header, else use server .env
    api_key = (x_openai_api_key or os.getenv("OPENAI_API_KEY", "")).strip()
    if not api_key:
        raise HTTPException(status_code=500, detail="Server missing OPENAI_API_KEY")

    client = OpenAI(api_key=api_key)
    model = req.model or "gpt-4o-mini"
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are ResumeAI Coach. Provide precise, actionable guidance: resume improvement, "
                        "skill gaps, matching roles based on provided analysis, and concrete next steps."
                    ),
                },
                *[{"role": m.role, "content": m.content} for m in req.messages],
            ],
            max_tokens=800,
            temperature=0.7,
        )
        content = completion.choices[0].message.content or ""
        return ChatResponse(content=content)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"OpenAI error: {exc}")



