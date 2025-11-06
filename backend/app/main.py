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


JobCategory = Tuple[str, List[Tuple[str, float]]]  # (keyword, weight)

CATEGORIES: List[JobCategory] = [
    ("Data Science", [
        ("machine learning", 3.0), ("data science", 3.0), ("data scientist", 2.5),
        ("python", 2.0), ("pandas", 2.0), ("numpy", 2.0), ("tensorflow", 2.5), ("pytorch", 2.5),
        ("statistics", 2.0), ("sql", 1.5), ("scikit-learn", 2.0), ("jupyter", 2.0),
        ("data analysis", 2.0), ("data visualization", 2.0), ("neural network", 2.5),
        ("deep learning", 2.5), ("nlp", 2.0), ("natural language processing", 2.0)
    ]),
    ("Software Engineering", [
        ("software engineer", 3.0), ("software developer", 3.0), ("full stack", 2.5),
        ("javascript", 2.0), ("typescript", 2.0), ("react", 2.0), ("node.js", 2.0), ("nodejs", 2.0),
        ("java", 2.0), ("spring", 2.0), ("c++", 1.5), ("c#", 1.5), (".net", 2.0),
        ("go", 2.0), ("golang", 2.0), ("rust", 2.0), ("microservices", 2.0),
        ("rest api", 1.5), ("graphql", 2.0), ("docker", 1.5), ("kubernetes", 1.5),
        ("git", 0.5), ("version control", 0.5), ("agile", 1.0), ("scrum", 1.0)
    ]),
    ("DevOps / Cloud", [
        ("devops", 3.0), ("cloud engineer", 3.0), ("sre", 2.5), ("site reliability", 2.5),
        ("aws", 2.5), ("amazon web services", 2.0), ("azure", 2.5), ("gcp", 2.5), ("google cloud", 2.0),
        ("terraform", 2.5), ("ansible", 2.5), ("kubernetes", 2.5), ("k8s", 2.0),
        ("ci/cd", 2.5), ("jenkins", 2.0), ("github actions", 2.0), ("gitlab ci", 2.0),
        ("docker", 2.0), ("containerization", 2.0), ("linux", 1.5), ("bash", 1.5),
        ("monitoring", 2.0), ("prometheus", 2.0), ("grafana", 2.0)
    ]),
    ("Product Management", [
        ("product manager", 3.0), ("product management", 3.0), ("product owner", 2.5),
        ("roadmap", 2.5), ("stakeholder", 2.0), ("product strategy", 2.5),
        ("metrics", 2.0), ("kpi", 2.0), ("user research", 2.5), ("user experience", 2.0),
        ("backlog", 2.0), ("agile", 1.5), ("scrum", 1.5), ("kanban", 1.5),
        ("mvp", 2.0), ("minimum viable product", 2.0), ("a/b testing", 2.0)
    ]),
    ("UI/UX Design", [
        ("ui designer", 3.0), ("ux designer", 3.0), ("user experience", 3.0), ("user interface", 3.0),
        ("figma", 2.5), ("sketch", 2.5), ("adobe xd", 2.5), ("prototype", 2.5),
        ("wireframe", 2.5), ("usability", 2.0), ("design system", 2.5),
        ("adobe", 1.5), ("photoshop", 1.5), ("illustrator", 1.5),
        ("interaction design", 2.5), ("user research", 2.0), ("persona", 2.0)
    ]),
    ("Data Engineering", [
        ("data engineer", 3.0), ("data engineering", 3.0), ("etl", 2.5),
        ("spark", 2.5), ("apache spark", 2.5), ("airflow", 2.5), ("kafka", 2.5),
        ("hadoop", 2.5), ("data pipeline", 2.5), ("data warehouse", 2.5),
        ("snowflake", 2.5), ("redshift", 2.5), ("databricks", 2.5),
        ("big data", 2.0), ("data lake", 2.0), ("pyspark", 2.0)
    ]),
    ("Cybersecurity", [
        ("cybersecurity", 3.0), ("security engineer", 3.0), ("information security", 3.0),
        ("siem", 2.5), ("soc", 2.5), ("security operations", 2.5),
        ("incident response", 2.5), ("vulnerability", 2.0), ("penetration testing", 2.5),
        ("nist", 2.0), ("owasp", 2.0), ("splunk", 2.0), ("iso 27001", 2.0),
        ("threat detection", 2.5), ("security audit", 2.0)
    ]),
]


def predict_category(text: str) -> PredictionResponse:
    """Predict category using ML model if available; fallback to weighted heuristic keywords."""
    # Try ML model first (primary method)
    if _ml_pipeline is not None and _ml_label_list is not None:
        try:
            # Get prediction probabilities
            proba = _ml_pipeline.predict_proba([text])[0]
            top_idx = int(proba.argmax())
            category = _ml_label_list[top_idx]
            confidence = float(proba[top_idx])
            
            # Get top 3 predictions for better insight
            top_3_indices = proba.argsort()[-3:][::-1]
            top_3_categories = [_ml_label_list[i] for i in top_3_indices]
            top_3_probs = [float(proba[i]) for i in top_3_indices]
            
            # Extract skills via heuristic
            skills_display = extract_skills(text)
            
            # Log prediction for debugging (can be removed in production)
            if confidence < 0.6:
                print(f"ML prediction confidence low ({confidence:.2%}), top 3: {list(zip(top_3_categories, [f'{p:.2%}' for p in top_3_probs]))}")
            
            return PredictionResponse(category=category, confidence=round(confidence, 2), skills=skills_display)
        except Exception as exc:
            print(f"ML prediction failed, using heuristic fallback: {exc}")
            import traceback
            traceback.print_exc()
            # fall through to heuristic
            pass

    # Weighted heuristic fallback
    import re
    text_lower = text.lower()
    best_category = "General"
    best_score = 0.0
    best_skills: List[str] = []

    for category, keywords in CATEGORIES:
        score = 0.0
        matched: List[str] = []
        for kw, weight in keywords:
            # Use word boundaries for better matching (avoid partial matches)
            # For multi-word phrases, use simple substring matching
            if ' ' in kw:
                # Multi-word phrase
                if kw in text_lower:
                    score += weight
                    matched.append(kw)
            else:
                # Single word - use word boundary regex
                pattern = r'\b' + re.escape(kw) + r'\b'
                if re.search(pattern, text_lower):
                    score += weight
                    matched.append(kw)
        
        if score > best_score:
            best_score = score
            best_category = category
            best_skills = matched

    # Normalize confidence (scores are weighted, so we adjust the calculation)
    max_possible_score = sum(max(weight for _, weight in keywords) for _, keywords in CATEGORIES if keywords)
    confidence = min(0.95, max(0.5, 0.5 + (best_score / max(10.0, max_possible_score * 0.3))))
    skills_display = [s.title() for s in best_skills][:15] if best_skills else ["Communication", "Teamwork"]

    return PredictionResponse(category=best_category, confidence=round(confidence, 2), skills=skills_display)


def extract_skills(text: str) -> List[str]:
    import re
    text_lower = text.lower()
    matched: List[str] = []
    for _, keywords in CATEGORIES:
        for kw, _ in keywords:
            # Use word boundaries for single words, substring for phrases
            if ' ' in kw:
                if kw in text_lower and kw not in matched:
                    matched.append(kw)
            else:
                pattern = r'\b' + re.escape(kw) + r'\b'
                if re.search(pattern, text_lower) and kw not in matched:
                    matched.append(kw)
    display = [s.title() for s in matched][:15]
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
    """Load and train ML model from resume dataset."""
    global _ml_pipeline, _ml_label_list

    if not (pd and TfidfVectorizer and LogisticRegression and Pipeline):
        print("WARNING: sklearn/pandas not available, using heuristic fallback")
        return  # sklearn/pandas missing

    # Try multiple possible paths for the dataset
    possible_paths = [
        # Path when running from backend directory (local dev)
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "../src/assets/resume-dataset.csv"),
        # Path when running from project root
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "src/assets/resume-dataset.csv"),
        # Path when deployed (if dataset is copied to backend)
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "resume-dataset.csv"),
        # Absolute fallback
        "src/assets/resume-dataset.csv",
    ]
    
    dataset_path = None
    for path in possible_paths:
        abs_path = os.path.abspath(path)
        if os.path.exists(abs_path):
            dataset_path = abs_path
            break
    
    if not dataset_path:
        print("WARNING: Dataset not found at any expected location, using heuristic fallback")
        print(f"Searched paths: {possible_paths}")
        return

    try:
        print(f"Loading dataset from: {dataset_path}")
        df = pd.read_csv(dataset_path, encoding='utf-8', on_bad_lines='skip')
        
        if "Category" not in df.columns or "Resume" not in df.columns:
            print(f"WARNING: Dataset missing required columns. Found: {df.columns.tolist()}")
            return
        
        # Clean data
        df = df.dropna(subset=["Category", "Resume"]).reset_index(drop=True)
        df = df[df["Resume"].astype(str).str.len() > 50]  # Filter very short resumes
        
        if len(df) < 10:
            print(f"WARNING: Dataset too small ({len(df)} rows), need at least 10 samples")
            return
        
        texts: List[str] = df["Resume"].astype(str).tolist()
        labels: List[str] = df["Category"].astype(str).str.strip().tolist()

        # Normalize category names
        category_mapping = {
            "Data Science": "Data Science",
            "data science": "Data Science",
            "Data Scientist": "Data Science",
            "Software Engineering": "Software Engineering",
            "software engineering": "Software Engineering",
            "Software Developer": "Software Engineering",
            "DevOps": "DevOps / Cloud",
            "DevOps / Cloud": "DevOps / Cloud",
            "Cloud Engineer": "DevOps / Cloud",
            "Product Management": "Product Management",
            "Product Manager": "Product Management",
            "UI/UX Design": "UI/UX Design",
            "UI Designer": "UI/UX Design",
            "UX Designer": "UI/UX Design",
            "Data Engineering": "Data Engineering",
            "Data Engineer": "Data Engineering",
            "Cybersecurity": "Cybersecurity",
            "Security Engineer": "Cybersecurity",
        }
        
        labels = [category_mapping.get(label, label) for label in labels]
        _ml_label_list = sorted(list(set(labels)))
        
        print(f"Training ML model on {len(texts)} resumes with {len(_ml_label_list)} categories: {_ml_label_list}")

        # Improved pipeline with better parameters
        pipeline = Pipeline([
            ("tfidf", TfidfVectorizer(
                ngram_range=(1, 3),  # Include trigrams for better context
                min_df=2,  # Minimum document frequency
                max_features=10000,  # Limit features for performance
                stop_words='english',  # Remove common English words
                lowercase=True,
                strip_accents='unicode'
            )),
            ("clf", LogisticRegression(
                max_iter=2000,  # More iterations for convergence
                n_jobs=-1,  # Use all CPUs
                verbose=0,
                C=1.0,  # Regularization strength
                solver='lbfgs',  # Good for multi-class
                multi_class='multinomial'
            )),
        ])

        pipeline.fit(texts, labels)
        _ml_pipeline = pipeline
        
        # Evaluate model performance
        from sklearn.model_selection import cross_val_score
        scores = cross_val_score(pipeline, texts, labels, cv=5, scoring='accuracy')
        print(f"ML Model trained successfully! Cross-validation accuracy: {scores.mean():.2%} (+/- {scores.std() * 2:.2%})")
        
    except Exception as exc:
        print(f"ERROR: Failed to train ML model: {exc}")
        import traceback
        traceback.print_exc()
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



