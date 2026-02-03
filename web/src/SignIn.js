import React, { useState } from "react";
import axios from "axios";
import { useNavigate, Link } from "react-router-dom";

function SignIn() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const API_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000";
      const res = await axios.post(`${API_URL}/api/login/`, { username, password });
      
      localStorage.setItem("token", res.data.token);
      navigate("/dashboard");
    } catch (err) {
      alert("Invalid credentials");
    }
  };

  return (
    <div className="glass-panel" style={{maxWidth: '400px', margin: '100px auto', textAlign: 'center'}}>
      <h2 className="section-title">Login</h2>
      <form onSubmit={handleLogin} style={{display:'flex', flexDirection:'column', gap:'15px'}}>
        <input className="input-field" placeholder="Username" onChange={e => setUsername(e.target.value)} />
        <input className="input-field" type="password" placeholder="Password" onChange={e => setPassword(e.target.value)} />
        <button type="submit" className="btn-gradient">Login</button>
      </form>
      <p style={{marginTop:'15px', color:'#ccc'}}>
        No account? <Link to="/signup" style={{color:'#f59e0b'}}>Sign Up</Link>
      </p>
    </div>
  );
}

export default SignIn;