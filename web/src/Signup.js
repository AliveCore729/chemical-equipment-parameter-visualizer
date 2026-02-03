import React, { useState } from "react";
import axios from "axios";
import { useNavigate, Link } from "react-router-dom";

function Signup() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSignup = async (e) => {
    e.preventDefault();
    try {
      const API_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000";
      await axios.post(`${API_URL}/api/register/`, { username, password });
      alert("Account created! Please login.");
      navigate("/");
    } catch (err) {
      alert("Error creating account. User might exist.");
    }
  };

  return (
    <div className="glass-panel" style={{maxWidth: '400px', margin: '100px auto', textAlign: 'center'}}>
      <h2 className="section-title">Sign Up</h2>
      <form onSubmit={handleSignup} style={{display:'flex', flexDirection:'column', gap:'15px'}}>
        <input className="input-field" placeholder="Username" onChange={e => setUsername(e.target.value)} />
        <input className="input-field" type="password" placeholder="Password" onChange={e => setPassword(e.target.value)} />
        <button type="submit" className="btn-gradient">Create Account</button>
      </form>
      <p style={{marginTop:'15px', color:'#ccc'}}>
        Have an account? <Link to="/" style={{color:'#f59e0b'}}>Login</Link>
      </p>
    </div>
  );
}

export default Signup;