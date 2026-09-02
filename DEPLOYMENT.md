# 🚀 Nivra Production Deployment Guide

This guide details all top production deployment options for **Nivra** across cloud platforms.

---

## 🌟 Option 1: Netlify (Best & Easiest for React Frontend)

Netlify provides zero-config, high-speed CDN hosting for the React frontend with automatic API routing.

### Steps:
1. Log in to [Netlify.com](https://www.netlify.com/).
2. Click **Add new site** → **Import an existing project** → Select **GitHub**.
3. Pick your repository: `Nikhat-syed/nivra-rag`.
4. Netlify automatically detects `netlify.toml` and configures:
   - **Build command**: `cd frontend && npm install && npm run build`
   - **Publish directory**: `frontend/dist`
5. Click **Deploy Site**!

---

## ⚡ Option 2: Koyeb (Best Free Serverless Docker Cloud for FastAPI Backend)

Koyeb automatically builds your Docker container directly from GitHub with built-in health checks.

### Steps:
1. Log in to [Koyeb.com](https://www.koyeb.com/).
2. Click **Create App** → Select **GitHub**.
3. Pick `Nikhat-syed/nivra-rag`.
4. Select **Dockerfile**: Set path to `backend/Dockerfile` (Port `8080`).
5. Set Environment Variables (`GROQ_API_KEY`, `SUPABASE_URL`, `SUPABASE_KEY`).
6. Click **Deploy**!

---

## 🎈 Option 3: Streamlit Community Cloud (1-Click Standalone Python Deployment)

Deploy the Python Streamlit version of Nivra in 1 click for free:

### Steps:
1. Log in to [share.streamlit.io](https://share.streamlit.io/).
2. Click **New app**.
3. Enter details:
   - **Repository**: `Nikhat-syed/nivra-rag`
   - **Branch**: `main`
   - **Main file path**: `app/main.py`
4. Click **Deploy**!

---

## 🐋 Option 4: Full Local / VPS Docker Compose

### Execution Steps
```bash
git clone https://github.com/Nikhat-syed/nivra-rag.git
cd nivra-rag
docker-compose up -d --build
```
- **React Nginx Web App**: `http://localhost` (Port 80)
- **FastAPI Backend Server**: `http://localhost:8080`
