from fastapi import FastAPI, File, UploadFile, Form
import cv2
import numpy as np
from PIL import Image
import io
import face_recognition
import json

from passlib.context import CryptContext
from datetime import datetime

from database import engine, SessionLocal
from models import Base, User, Attendance

# ✅ CREATE TABLES
Base.metadata.create_all(bind=engine)

# ✅ FASTAPI APP
app = FastAPI()

# ✅ PASSWORD HASH
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# =====================================
# HOME ROUTE
# =====================================

@app.get("/")
def home():
    return {
        "message": "Face Attendance API Running ✅"
    }

# =====================================
# TEST ROUTE
# =====================================

@app.get("/test")
def test():
    return {
        "status": "working ✅"
    }

# =====================================
# CREATE USER
# =====================================

@app.post("/create-user")
def create_user(
    username: str = Form(...),
    password: str = Form(...),
    role: str = Form("student")
):

    db = SessionLocal()

    password = password[:72]

    hashed_password = pwd_context.hash(password)

    user = User(
        username=username,
        password=hashed_password,
        role=role
    )

    db.add(user)
    db.commit()
    db.close()

    return {
        "message": "User created ✅"
    }

# =====================================
# DETECT FACE
# =====================================

@app.post("/detect-face")
async def detect_face(
    file: UploadFile = File(...)
):

    contents = await file.read()

    image = Image.open(
        io.BytesIO(contents)
    ).convert("RGB")

    img = np.array(image)

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_RGB2GRAY
    )

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades +
        "haarcascade_frontalface_default.xml"
    )

    faces = face_cascade.detectMultiScale(
        gray,
        1.3,
        5
    )

    return {
        "faces_detected": len(faces),
        "message":
        "Face Detected ✅"
        if len(faces) > 0
        else "No Face Found ❌"
    }

# =====================================
# LOGIN
# =====================================

@app.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...)
):

    db = SessionLocal()

    user = db.query(User).filter(
        User.username == username
    ).first()

    if not user:

        db.close()

        return {
            "status": "error",
            "message": "User not found ❌"
        }

    password = password[:72]

    if not pwd_context.verify(
        password,
        user.password
    ):

        db.close()

        return {
            "status": "error",
            "message": "Wrong password ❌"
        }

    db.close()

    return {
        "status": "success",
        "message": "Login successful ✅",
        "role": user.role,
        "name": user.name
    }

# =====================================
# REGISTER WITH FACE
# =====================================

@app.post("/register-with-face")
async def register_with_face(

    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    department: str = Form(...),
    year: str = Form(...),
    address: str = Form(...),

    username: str = Form(...),
    password: str = Form(...),

    file: UploadFile = File(...)
):

    db = SessionLocal()

    existing_user = db.query(User).filter(
        User.username == username
    ).first()

    if existing_user:

        db.close()

        return {
            "status": "error",
            "message":
            "Username already exists ⚠️"
        }

    contents = await file.read()

    image = Image.open(
        io.BytesIO(contents)
    ).convert("RGB")

    img = np.array(image)

    encodings = face_recognition.face_encodings(img)

    if len(encodings) == 0:

        db.close()

        return {
            "message":
            "No face detected ❌"
        }

    encoding = encodings[0].tolist()

    password = password[:72]

    hashed_password = pwd_context.hash(password)

    user = User(

        name=name,
        email=email,
        phone=phone,
        department=department,
        year=year,
        address=address,

        username=username,

        password=hashed_password,

        face_encoding=
        json.dumps(encoding),

        role="student"
    )

    db.add(user)

    db.commit()

    db.close()

    return {
        "status": "success",
        "message":
        "User registered successfully ✅"
    }

# =====================================
# RECOGNIZE FACE
# =====================================

@app.post("/recognize")
async def recognize(

    file: UploadFile = File(...),

    latitude: str = Form(...),

    longitude: str = Form(...),

    action: str = Form(...)
):

    db = SessionLocal()

    try:

        contents = await file.read()

        image = Image.open(
            io.BytesIO(contents)
        ).convert("RGB")

        img = np.array(image)

        encodings = face_recognition.face_encodings(img)

        if len(encodings) == 0:

            return {
                "message":
                "No face detected ❌"
            }

        unknown_encoding = encodings[0]

        users = db.query(User).all()

        for user in users:

            if not user.face_encoding:
                continue

            stored_encoding = np.array(
                json.loads(user.face_encoding)
            )

            distance_face = face_recognition.face_distance(
                [stored_encoding],
                unknown_encoding
            )[0]

            if distance_face < 0.5:

                user_name = user.name

                now = datetime.now()

                today_date = now.strftime("%Y-%m-%d")

                current_time = now.strftime("%H:%M:%S")

                existing = db.query(Attendance).filter(

                    Attendance.name ==
                    user_name,

                    Attendance.date ==
                    today_date

                ).first()

                # ✅ CHECK IN
                if action == "check_in":

                    if existing:

                        return {
                            "message": f"{user_name} already checked in ⚠️",

                            "type":
                            "already_checkin"
                        }

                    attendance = Attendance(

                        name=user_name,

                        date=today_date,

                        check_in=current_time,

                        check_out="",

                        latitude=latitude,

                        longitude=longitude
                    )

                    db.add(attendance)

                    db.commit()

                    return {
                        "message":
                        f"Check-in marked for {user_name} ✅",

                        "type":
                        "check_in"
                    }

                # ✅ CHECK OUT
                elif action == "check_out":

                    if not existing:

                        return {
                            "message":
                            "Please check in first ❌",

                            "type":
                            "error"
                        }

                    if existing.check_out:

                        return {
                            "message": f"{user_name} already checked out ⚠️",

                            "type":
                            "already_checkout"
                        }

                    existing.check_out = current_time

                    db.commit()

                    return {
                        "message":
                        f"Check-out marked for {user_name} ✅",

                        "type":
                        "check_out"
                    }

        return {
            "message":
            "Unknown person ❌"
        }

    finally:

        db.close()

# =====================================
# GET ATTENDANCE
# =====================================

@app.get("/attendance")
def get_attendance():

    db = SessionLocal()

    records = db.query(Attendance).all()

    data = []

    for r in records:

        data.append({

            "name": r.name,

            "date": r.date,

            "check_in": r.check_in,

            "check_out": r.check_out,

            "latitude": r.latitude,

            "longitude": r.longitude
        })

    db.close()

    return data

# =====================================
# GET STUDENTS
# =====================================

@app.get("/students")
def get_students():

    db = SessionLocal()

    users = db.query(User).all()

    data = []

    for u in users:

        data.append({

            "username": u.username,

            "role": u.role
        })

    db.close()

    return data