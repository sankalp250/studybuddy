# 🎓 StudyBuddy AI - Interview Preparation Guide

This guide is designed to help you explain the **StudyBuddy AI** project during your technical interview. It covers the problem statement, solution architecture, technical challenges, and key features.

---

## 1. 🚀 Project Elevator Pitch
> "StudyBuddy AI is an intelligent learning ecosystem designed to help students maximize their study efficiency. It combines **Generative AI** for personalized content creation with a **Spaced Repetition System (SRS)** for long-term memory retention. Unlike generic chatbots, it builds a knowledge graph of your learning goals and actively manages your review schedule."

---

## 2. 🏗️ System Architecture

### **Tech Stack**
- **Frontend**: Streamlit (Python-based UI for rapid data apps)
- **Backend**: FastAPI (High-performance Async Python API)
- **Database**: PostgreSQL (Neon Serverless)
- **AI/LLM**: 
  - **LangChain** (Orchestration)
  - **Groq** (Llama 3 8B - High-speed inference)
  - **Tavily** (Real-time Web Search)
- **Deployment**: Render (Backend) & Streamlit Cloud (Frontend)

### **Key Components**
1. **RAG Engine (Retrieval-Augmented Generation)**:
   - *What it does*: Ingests your Resume (PDF) and creates a vector index.
   - *Why*: Allows the AI to generate interview questions *contextually relevant* to your actual experience.
   - *Tech*: PyMuPDF (extraction) -> Text Splitter -> FastEmbed/ChromaDB (Vector Store).

2. **Spaced Repetition System (SRS)**:
   - *What it does*: Schedules flashcard reviews based on how well you know them.
   - *Algorithm*: Modified SuperMemo-2 (SM-2). 
   - *Logic*: `Next Review = F(Current Interval, Ease Factor, Grade)`.
   - *Impact*: Optimizes memory retention by engaging you just before you forget.

3. **Multi-Agent System**:
   - **Interview Agent**: Simulates technical interviews.
   - **Resume Agent**: Analyzes resumes for skills/gaps.
   - **Daily Digest Agent**: Fetches latest tech news (using Tavily Search).

---

## 3. ✨ Key Features to Demo

### **A. Real-Time Analytics (The "New" Feature)**
- **Feature**: Shows live stats of your study habits.
- **Explain**: "I recently implemented a real-time analytics dashboard that aggregates data from the PostgreSQL database. It calculates total review time, card distribution, and completion rates using SQL aggregations via SQLAlchemy."

### **B. Resume-Based Interview Prep**
- **Feature**: Upload resume -> Get asked about *your* projects.
- **Explain**: "The system uses RAG to chunk my resume, embed it into a vector store, and retrieve relevant sections when generating questions. This ensures the AI acts like a hiring manager reading my specific CV."

### **C. AI Flashcard Generation**
- **Feature**: Chat about a topic -> Click "Create Flashcards".
- **Explain**: "The AI extracts key concepts from our conversation and formats them into Q&A pairs, which are then saved to the database with an initial SRS interval."

---

## 4. 🔧 Technical Challenges & Solutions

| Challenge | Solution |
|-----------|----------|
| **Deployment Issues on Linux** | *Problem*: `requirements.txt` was UTF-16 encoded (Windows default), causing Docker build failures. <br>*Fix*: Re-encoded to UTF-8 and fixed specific dependency versions (bcrypt/chromadb conflict). |
| **Performance (Cold Starts)** | *Problem*: RAG model loading was slow on serverless. <br>*Fix*: Optimized by allowing RAG to be toggled via env vars and using lighter embedding models (`FastEmbed`). |
| **Database Migration** | *Problem*: Schema changes during development. <br>*Fix*: Used **Alembic** for auto-generating migration scripts (`alembic upgrade head` on startup). |

---

## 5. 🔮 Future Roadmap
- **React Migration**: Moving frontend to React/Next.js for better interactivity.
- **Voice Mode**: Adding audio input/output for mock interviews.
- **Multi-User Teams**: allowing study groups to share decks.

---

**Good luck with your interview! You built a full-stack AI application with real database management and complex logic. Be proud of it!** 🚀
