from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from jose import JWTError, jwt
from datetime import datetime, timedelta

# Secret key
SECRET_KEY = "my_secret_key_123"
ALGORITHM = "HS256"

app = FastAPI()

# CORS (allow React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- AUTH ----------

class LoginRequest(BaseModel):
    email: str
    password: str

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=30)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.get("/")
def root():
    return {"message": "Backend is running"}

@app.post("/api/login")
def login(data: LoginRequest):
    if data.email == "test@demo.com" and data.password == "1234":
        token = create_access_token({"sub": data.email})
        return {"status": "success", "token": token}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/api/profile")
def get_profile(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email = payload.get("sub")

        if user_email is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return {
            "username": "Test User",
            "age": 22,
            "role": "student"
        }

    except JWTError:
        raise HTTPException(status_code=401, detail="Token verification failed")

# ---------- STUDENTS ----------

students = [
    {"id": 1, "name": "Mansi", "age": 21},
    {"id": 2, "name": "Dikshant", "age": 22}
]

class Student(BaseModel):
    name: str
    age: int

@app.get("/api/students")
def get_students():
    return students

@app.post("/api/students")
def add_student(student: Student):
    new_id = len(students) + 1
    new_student = {"id": new_id, "name": student.name, "age": student.age}
    students.append(new_student)
    return {"message": "Student added", "student": new_student}

@app.put("/api/students/{student_id}")
def update_student(student_id: int, student: Student):
    for s in students:
        if s["id"] == student_id:
            s["name"] = student.name
            s["age"] = student.age
            return {"message": "Student updated", "student": s}

    raise HTTPException(status_code=404, detail="Student not found")

@app.delete("/api/students/{student_id}")
def delete_student(student_id: int):
    for s in students:
        if s["id"] == student_id:
            students.remove(s)
            return {"message": "Student deleted"}

    raise HTTPException(status_code=404, detail="Student not found")
