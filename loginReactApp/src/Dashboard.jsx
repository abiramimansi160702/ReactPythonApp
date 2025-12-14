import { useEffect, useState } from "react";
import "./Dashboard.css";

function Dashboard({ token }) {
  const [userData, setUserData] = useState(null);
  const [students, setStudents] = useState([]);
  const [name, setName] = useState("");
  const [age, setAge] = useState("");

  // Edit state
  const [editingId, setEditingId] = useState(null);
  const [editName, setEditName] = useState("");
  const [editAge, setEditAge] = useState("");

  // Fetch profile
  useEffect(() => {
    fetch("http://13.49.224.125:8000/profile?token=" + token)
      .then(res => res.json())
      .then(data => setUserData(data))
      .catch(err => console.error(err));
  }, []);

  // Fetch students
  const fetchStudents = () => {
    fetch("http://13.49.224.125:8000/students")
      .then(res => res.json())
      .then(data => setStudents(data))
      .catch(err => console.error(err));
  };

  useEffect(() => {
    fetchStudents();
  }, []);

  // Add student
  const addStudent = () => {
    if (!name || !age) {
      alert("Please enter name and age");
      return;
    }

    fetch("http://13.49.224.125:8000/students", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, age: Number(age) })
    })
      .then(res => res.json())
      .then(data => {
        alert("Student added!");
        setStudents([...students, data.student]);
        setName("");
        setAge("");
      });
  };

  // Delete student
  const deleteStudent = (id) => {
    fetch(`http://13.49.224.125:8000/students/${id}`, { method: "DELETE" })
      .then(res => res.json())
      .then(() => setStudents(students.filter(s => s.id !== id)));
  };

  // Start editing
  const startEdit = (student) => {
    setEditingId(student.id);
    setEditName(student.name);
    setEditAge(student.age);
  };

  // Save edited student
  const saveEdit = (id) => {
    fetch(`http://13.49.224.125:8000/students/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: editName, age: Number(editAge) })
    })
      .then(res => {
        if (!res.ok) throw new Error("Update failed");
        return res.json();
      })
      .then(() => {
        setEditingId(null);
        fetchStudents(); // refresh list
      })
      .catch(err => alert("Update failed: " + err));
  };

  if (!userData) return <h2>Loading dashboard...</h2>;

  return (
    <div className="dashboard-container">
      {/* Profile */}
      <div className="profile-card">
        <h1>Welcome, {userData.username}!</h1>
        <p>Age: {userData.age}</p>
        <p>Role: {userData.role}</p>
      </div>

      {/* Add Student */}
      <div className="add-student-card">
        <h2>Add Student</h2>
        <input
          type="text"
          placeholder="Enter name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <input
          type="number"
          placeholder="Enter age"
          value={age}
          onChange={(e) => setAge(e.target.value)}
        />
        <button onClick={addStudent}>Add Student</button>
      </div>

      {/* Students List */}
      <div className="students-list-card">
        <h2>Students List</h2>
        <ul>
          {students.map((s) => (
            <li key={s.id} className="student-item">
              {editingId === s.id ? (
                <>
                  <input
                    type="text"
                    value={editName}
                    onChange={(e) => setEditName(e.target.value)}
                  />
                  <input
                    type="number"
                    value={editAge}
                    onChange={(e) => setEditAge(e.target.value)}
                  />
                  <button onClick={() => saveEdit(s.id)}>Save</button>
                  <button onClick={() => setEditingId(null)}>Cancel</button>
                </>
              ) : (
                <>
                  {s.name} - {s.age} years
                  <div>
                    <button onClick={() => startEdit(s)}>Edit</button>
                    <button onClick={() => deleteStudent(s.id)}>Delete</button>
                  </div>
                </>
              )}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default Dashboard;
