from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from jose import JWTError, jwt
from datetime import datetime, timedelta

# Secret key to create tokens (can be anything random)
SECRET_KEY = "my_secret_key_123"
ALGORITHM = "HS256"

app = FastAPI()

# Allow React to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model for login data
class LoginRequest(BaseModel):
    email: str
    password: str

# Function to create token
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=30)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

# Login route
@app.post("/login")
def login(data: LoginRequest):
    if data.email == "test@demo.com" and data.password == "1234":
        # Create a token for this user
        token = create_access_token({"sub": data.email})
        return {"status": "success", "token": token}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

# Protected route
@app.get("/profile")
def get_profile(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email = payload.get("sub")

        if user_email is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Return dummy data
        return {"username": "Test User", "age": 22, "role": "student"}
    except JWTError:
        raise HTTPException(status_code=401, detail="Token verification failed")

students = [
    {"id": 1, "name": "Mansi", "age": 21},
    {"id": 2, "name": "Dikshant", "age": 22}
]
@app.get("/students")
def get_students():
    return students

class Student(BaseModel):
    name: str
    age: int

@app.post("/students")
def add_student(student: Student):
    new_id = len(students) + 1
    new_student = {"id": new_id, "name": student.name, "age": student.age}
    students.append(new_student)
    return {"message": "Student added", "student": new_student}

@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):
    for s in students:
        if s["id"] == student_id:
            s["name"] = student.name
            s["age"] = student.age
            return {"message": "Student updated", "student": s}

    raise HTTPException(status_code=404, detail="Student not found")

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    for s in students:
        if s["id"] == student_id:
            students.remove(s)
            return {"message": "Student deleted"}

    raise HTTPException(status_code=404, detail="Student not found")
