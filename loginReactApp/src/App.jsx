import { useState } from "react";
import Dashboard from "./Dashboard";
import "./App.css";

// ✅ Use your ALB URL
const API_URL = "http://login-react-alb-337425369.eu-north-1.elb.amazonaws.com";

function App() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [token, setToken] = useState(null);

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`${API_URL}/api/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: username, password }),
      });

      if (response.ok) {
        const data = await response.json();
        setToken(data.token); // save token
      } else {
        alert("Login failed! Check your credentials.");
      }
    } catch (err) {
      console.error("Error connecting to backend:", err);
      alert("Cannot reach backend server.");
    }
  };

  if (token) {
    return <Dashboard token={token} />;
  }

  return (
    <div className="login-container">
      <h2 className="login-title">Welcome Back!</h2>
      <form onSubmit={handleLogin} className="login-form">
        <input
          type="email"
          placeholder="Email"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit">Login</button>
      </form>
    </div>
  );
}

export default App;
