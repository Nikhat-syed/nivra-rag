# 🚀 Nivra Production Deployment Guide

This guide provides step-by-step instructions for deploying **Nivra** in production environments.

---

## 🐋 Option 1: Full Docker & Docker Compose Deployment (Recommended)

### Prerequisites
- Docker Engine & Docker Compose installed.

### Execution Steps
1. **Clone the repository & enter root directory**:
   ```bash
   cd "rag system"
   ```

2. **Configure Environment Variables**:
   Create a `.env` file from template:
   ```bash
   cp .env.example .env
   ```
   Add your `GROQ_API_KEY`, `SUPABASE_URL`, and `SUPABASE_KEY` (optional).

3. **Build and Start Container Cluster**:
   ```bash
   docker-compose up -d --build
   ```

4. **Verify Container Services**:
   - **React Nginx Web App**: `http://localhost` (Port 80)
   - **FastAPI Backend Server**: `http://localhost:8080`
   - **Qdrant Vector Database**: `http://localhost:6333`
   - **Healthcheck Probe**: `http://localhost:8080/health`

5. **Stop Container Cluster**:
   ```bash
   docker-compose down
   ```

---

## ☁️ Option 2: Zero-Cost Hybrid Cloud (Vercel + Render)

### A. Deploy Frontend on Vercel (Global Edge Network)
1. Install Vercel CLI or connect your GitHub repository to [Vercel](https://vercel.com).
2. Run command:
   ```bash
   vercel
   ```
3. Vercel automatically detects `vercel.json` and builds `frontend/dist`.

### B. Deploy Backend on Render (FastAPI Cloud API)
1. Create a free account on [Render](https://render.com).
2. Click **New Web Service** and connect your GitHub repository.
3. Render automatically detects `render.yaml`:
   - **Environment**: Python 3.11
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python -m uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
   - **Healthcheck**: `/health`
4. Set Environment Variables (`GROQ_API_KEY`, `SUPABASE_URL`, `SUPABASE_KEY`).

---

## 🚂 Option 3: Railway / Fly.io One-Click Container Deployment

### Deploy via Railway CLI
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login and deploy
railway login
railway up
```

---

## 🔍 Post-Deployment Verification Checklist

- [x] Test `GET /health` returns `{"status":"healthy"}`.
- [x] Test scheme search and hybrid retrieval on production frontend.
- [x] Verify Supabase database bookmark synchronization across browser sessions.
- [x] Test plain-language rewrite and Telugu / Hindi multilingual translation.
