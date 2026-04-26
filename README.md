# Face Attendance Backend

A FastAPI-based backend for a Face Attendance System with face recognition, user management, attendance tracking, and Railway deployment support.

---

# Features

- Face Recognition Attendance
- User Registration with Face Data
- Check-In / Check-Out System
- FastAPI REST APIs
- SQLite Database Support
- Railway Deployment Ready
- OpenCV + face_recognition Integration
- Secure Password Hashing
- Docker Support

---

# Tech Stack

- Python
- FastAPI
- SQLAlchemy
- OpenCV
- face_recognition
- SQLite
- Uvicorn
- Docker
- Railway

---

# Project Structure

```bash
face-attendance-backend/
│
├── app.py
├── database.py
├── models.py
├── requirements.txt
├── Dockerfile
├── Procfile
├── .gitignore
└── README.md
```

---

# Installation

## 1. Clone Repository

```bash
git clone https://github.com/your-username/face-attendance-backend.git
cd face-attendance-backend
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / Mac

```bash
source venv/bin/activate
```

---

## 3. Install Requirements

```bash
pip install -r requirements.txt
```

---

# Run Backend

```bash
uvicorn app:app --reload
```

Backend will run on:

```bash
http://127.0.0.1:8000
```

---

# API Documentation

## Swagger UI

```bash
http://127.0.0.1:8000/docs
```

## ReDoc

```bash
http://127.0.0.1:8000/redoc
```

---

# Requirements

```txt
fastapi
uvicorn
numpy==1.26.4
opencv-python-headless
face_recognition
face_recognition_models
sqlalchemy
python-multipart
pillow
passlib==1.7.4
bcrypt==3.2.2
pytz
```

---

# Railway Deployment

## 1. Push Code to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin YOUR_REPOSITORY_URL
git push -u origin main
```

---

## 2. Deploy on Railway

1. Open Railway
2. Create New Project
3. Select "Deploy from GitHub Repo"
4. Select your repository
5. Railway will auto deploy

---

# Docker Setup

## Build Docker Image

```bash
docker build -t face-attendance-backend .
```

## Run Docker Container

```bash
docker run -p 8000:8000 face-attendance-backend
```

---

# Example Features

## User APIs

- Create User
- Login User
- Get All Users
- Delete User

## Attendance APIs

- Face Check-In
- Face Check-Out
- Attendance History

---

# Environment Variables

Create `.env` file if needed:

```env
DATABASE_URL=sqlite:///./attendance.db
```

---

# Common Errors Fix

## NumPy Compatibility Error

If `face_recognition` gives NumPy error:

```bash
pip install numpy==1.26.4
```

---

## dlib Installation Error

### Windows

Install:
- Visual Studio Build Tools
- CMake

### Linux

```bash
sudo apt-get install cmake
sudo apt-get install build-essential
```

---

# Run Using Procfile

```bash
web: uvicorn app:app --host 0.0.0.0 --port $PORT
```

---

# Author

Developed by Project Wala 🚀

---

# License

This project is licensed under the MIT License.
