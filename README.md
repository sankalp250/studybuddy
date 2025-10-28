# 🤖 StudyBuddy AI: Intelligent Learning Ecosystem

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.118+-green.svg)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.50+-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **An intelligent, full-stack application that transforms how students prepare for interviews and manage their learning journey through AI-powered personalization and scientifically-proven spaced repetition.**

### 🌐 **Live Application**
- **Frontend**: [https://studybuddy-pswv2yg6aasmxvgcfkpdcs.streamlit.app/](https://studybuddy-pswv2yg6aasmxvgcfkpdcs.streamlit.app/)
- **Backend API**: [https://studybuddy-backend-xodg.onrender.com/](https://studybuddy-backend-xodg.onrender.com/)
- **API Documentation**: [https://studybuddy-backend-xodg.onrender.com/docs](https://studybuddy-backend-xodg.onrender.com/docs)

### 🐳 **Docker Image**
```bash
docker pull sankalp250/studybuddy-backend
```

---

## 🌟 Overview

StudyBuddy AI is a comprehensive learning platform that combines cutting-edge AI technology with proven learning methodologies to create a personalized, proactive study experience. Built for students preparing for technical interviews, the platform leverages your resume, learning goals, and conversation history to deliver targeted preparation materials.

### 🎯 Key Value Propositions

- **Personalized Interview Prep**: AI generates custom questions based on your actual resume and experience
- **Spaced Repetition System**: Scientifically-proven algorithm maximizes long-term retention
- **Proactive Learning**: Converts conversations into flashcards automatically
- **Multi-Modal AI**: Combines web search, content generation, and personalized coaching
- **Enterprise-Ready**: Full authentication, database management, and scalable architecture

---

## ✨ Features

### 🧠 **Intelligent Interview Preparation**
- **Resume-Based Personalization**: Upload your resume for hyper-targeted interview questions
- **Dynamic Question Generation**: AI creates relevant questions based on your specific projects and skills
- **Conversational Learning**: Interactive chat sessions that adapt to your responses
- **Project-Specific Prep**: Deep dive into your actual work (e.g., Dynamic Pricing Engine with Prophet forecasting)

### 📚 **Spaced Repetition System (SRS)**
- **Automatic Flashcard Generation**: Converts AI conversations into study materials
- **Scientific Algorithm**: Implements proven spaced repetition for optimal retention
- **Performance Tracking**: Monitors your learning progress and adjusts review intervals
- **Due Card Management**: Smart scheduling ensures efficient study sessions

### 🔍 **AI-Powered Content Generation**
- **Daily Digest**: Real-time news summaries on any topic using web search
- **LeetCode Generator**: Creates original coding problems at any difficulty level
- **Resume Analysis**: AI-powered resume summarization and skill extraction
- **Multi-Agent Architecture**: Specialized AI agents for different learning tasks

### 🔐 **Enterprise-Grade Security**
- **JWT Authentication**: Secure token-based authentication system
- **User Data Isolation**: Complete privacy with user-specific data storage
- **Password Hashing**: Industry-standard bcrypt password security
- **Session Management**: Secure login/logout with token expiration

---

## 🛠️ Tech Stack

### **Backend Architecture**
- **Framework**: FastAPI (High-performance async API)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Migrations**: Alembic for database schema management
- **Authentication**: JWT tokens with OAuth2 password flow
- **Security**: Passlib for password hashing, python-jose for JWT

### **AI & Machine Learning**
- **Framework**: LangChain + LangGraph for agent orchestration
- **LLM Provider**: Groq (Llama 3.1 8B Instant)
- **Search Engine**: Tavily for real-time web search
- **Agent Architecture**: Multi-agent system with specialized roles

### **Frontend & UI**
- **Framework**: Streamlit (Multi-page application)
- **Styling**: Custom CSS with modern UI components
- **State Management**: Streamlit session state
- **File Handling**: PDF parsing with PyMuPDF

### **DevOps & Deployment**
- **Containerization**: Docker for backend services
- **Database**: PostgreSQL with connection pooling
- **Environment**: Python 3.12+ with virtual environment
- **Dependencies**: Comprehensive requirements.txt with pinned versions

---

## 🚀 Quick Start

### Prerequisites
- Python 3.12 or higher
- PostgreSQL 12+ 
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sankalp250/studybuddy-ai.git
   cd studybuddy-ai
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL database**
   ```sql
   CREATE DATABASE studybuddy_db;
   CREATE USER studybuddy_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE studybuddy_db TO studybuddy_user;
   ```

5. **Configure environment variables**
   ```bash
   # Create .env file
   cp .env.example .env
   ```
   
   Edit `.env` with your configuration:
   ```env
   DATABASE_URL=postgresql://studybuddy_user:your_password@localhost:5432/studybuddy_db
   SECRET_KEY=your-super-secret-jwt-key-here
   GROQ_API_KEY=your-groq-api-key
   TAVILY_API_KEY=your-tavily-api-key
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ALGORITHM=HS256
   ```

6. **Initialize database**
   ```bash
   alembic upgrade head
   ```

7. **Run the application**
   
   **Terminal 1 (Backend API):**
   ```bash
   uvicorn main:app --reload --host 127.0.0.1 --port 8000
   ```
   
**Terminal 2 (Frontend):**
```bash
streamlit run dashboard.py
```

8. **Access the application**
   - Frontend: http://localhost:8501
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### **🌐 Or Use the Live Application**
- **Frontend**: [https://studybuddy-pswv2yg6aasmxvgcfkpdcs.streamlit.app/](https://studybuddy-pswv2yg6aasmxvgcfkpdcs.streamlit.app/)
- **Backend API**: [https://studybuddy-backend-xodg.onrender.com/](https://studybuddy-backend-xodg.onrender.com/)
- **API Documentation**: [https://studybuddy-backend-xodg.onrender.com/docs](https://studybuddy-backend-xodg.onrender.com/docs)

---

## 📖 Usage Guide

### Getting Started
1. **Create Account**: Sign up with your email and password
2. **Upload Resume**: Go to Account page and upload your resume (PDF or text)
3. **Add Learning Goals**: Create todo items for topics you want to study
4. **Start AI Sessions**: Click "Discuss" on any todo to begin AI-powered preparation

### Key Workflows

#### **Interview Preparation**
```
1. Upload resume → AI analyzes your background
2. Add todo: "Data Science Interview Prep"
3. Click "Discuss" → AI generates personalized questions
4. Chat with AI → Get targeted practice questions
5. Generate flashcards → Convert conversation to study materials
```

#### **Spaced Repetition Learning**
```
1. Complete AI prep session
2. Click "Create Flashcards" → AI extracts key concepts
3. Review flashcards → Rate your performance (1-5)
4. SRS algorithm schedules next review
5. Repeat for optimal retention
```

---

## 🏗️ Architecture

### **System Architecture**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │   FastAPI       │    │   PostgreSQL   │
│   Frontend      │◄──►│   Backend       │◄──►│   Database     │
│   (Port 8501)   │    │   (Port 8000)   │    │   (Port 5432)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │
         │                       ▼
         │              ┌─────────────────┐
         │              │   AI Services   │
         │              │   - Groq LLM    │
         │              │   - Tavily      │
         │              │   - LangChain   │
         │              └─────────────────┘
         │
         ▼
┌─────────────────┐
│   User Session  │
│   Management    │
└─────────────────┘
```

### **AI Agent Architecture**
- **Interview Agent**: Specialized for interview preparation without external tools
- **Daily Digest Agent**: Web search and content summarization
- **LeetCode Agent**: Coding problem generation
- **Flashcard Agent**: Content-to-flashcard conversion
- **Resume Agent**: Resume analysis and summarization

---

## 🔧 API Documentation

### **Authentication Endpoints**
- `POST /api/token` - Login and get JWT token
- `POST /api/users/` - User registration

### **Core Features**
- `POST /api/agent/chat/` - AI interview preparation chat
- `POST /api/generate-flashcards/` - Convert conversations to flashcards
- `GET /api/flashcards/due/` - Get flashcards due for review
- `POST /api/flashcards/{id}/review/` - Submit flashcard review

### **Content Generation**
- `POST /api/daily-digest/` - Generate news summaries
- `POST /api/generate-leetcode/` - Create coding problems
- `POST /api/upload-resume/` - Process and summarize resume

### **Data Management**
- `GET /api/todos/` - Get user's todo items
- `POST /api/todos/` - Create new todo item
- `GET /api/resume-summary/` - Get processed resume summary

---

## 🧪 Testing

### **Run Tests**
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_api_endpoints.py

# Run with coverage
pytest --cov=studybuddy
```

### **Test Coverage**
- API endpoint testing
- Database CRUD operations
- Authentication flow
- AI agent functionality

---

## 🚀 Deployment

### **Current Production Deployment**
- **Frontend**: Streamlit Community Cloud ([Live App](https://studybuddy-pswv2yg6aasmxvgcfkpdcs.streamlit.app/))
- **Backend**: Render ([Live API](https://studybuddy-backend-xodg.onrender.com/))
- **Database**: PostgreSQL on Render
- **Docker**: [sankalp250/studybuddy-backend](https://hub.docker.com/r/sankalp250/studybuddy-backend)

### **Deployment Steps**
1. Backend is deployed on Render with auto-deploy from GitHub
2. Frontend is deployed on Streamlit Cloud with linked GitHub repository
3. Database migrations run automatically on backend startup

### **Environment Variables for Production**
```env
DATABASE_URL=postgresql://user:pass@host:port/db
SECRET_KEY=production-secret-key
GROQ_API_KEY=your-production-groq-key
TAVILY_API_KEY=your-production-tavily-key
ACCESS_TOKEN_EXPIRE_MINUTES=60
ALGORITHM=HS256
```

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### **Development Setup**
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Run tests: `pytest`
5. Commit changes: `git commit -m 'Add amazing feature'`
6. Push to branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **LangChain Team** for the excellent AI framework
- **Groq** for fast LLM inference
- **Streamlit** for the intuitive web framework
- **FastAPI** for the high-performance API framework
- **PostgreSQL** for reliable data storage

---

## 📞 Support

- **Documentation**: [Wiki](https://github.com/yourusername/studybuddy-ai/wiki)
- **Issues**: [GitHub Issues](https://github.com/yourusername/studybuddy-ai/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/studybuddy-ai/discussions)

---

## 🎯 Roadmap

### **Phase 1: Core Features** ✅
- [x] User authentication and management
- [x] AI-powered interview preparation
- [x] Spaced repetition system
- [x] Resume analysis and personalization

### **Phase 2: Enhanced AI** 🚧
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Integration with job boards
- [ ] Video interview preparation

### **Phase 3: Enterprise Features** 📋
- [ ] Team collaboration features
- [ ] Advanced reporting and analytics
- [ ] API rate limiting and monitoring
- [ ] Enterprise SSO integration

---

<div align="center">

**Built with ❤️ for students preparing for their dream careers**

[⭐ Star this repo](https://github.com/yourusername/studybuddy-ai) | [🐛 Report Bug](https://github.com/yourusername/studybuddy-ai/issues) | [💡 Request Feature](https://github.com/yourusername/studybuddy-ai/issues)

</div>
