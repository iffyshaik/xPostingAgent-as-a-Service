// Login.tsx
// Form that allows user to enter credentials and logs them in via backend API.

import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/AuthProvider";
import axios from "../api";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const navigate = useNavigate();
  const { login, isAuthenticated } = useAuth();

  // If already logged in, prevent showing the login page again
  useEffect(() => {
    if (isAuthenticated) {
      navigate("/dashboard");
    }
  }, [isAuthenticated, navigate]);

  if (isAuthenticated) {
    return null; // Or a loading spinner
  }

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    try {
      const response = await axios.post("/auth/login", {
        email,
        password,
      });

      const token = response.data?.data?.token;

      if (!token) {
        setError("Login failed: no token received.");
        return;
      }

      login(token);
      console.log("Token saved. Redirecting via useEffect.");
    } catch (err: any) {
      console.error(err);
      setError("Invalid email or password.");
    }
  };

return (
  <div className="min-h-screen flex items-center justify-center bg-gray-100">
    <div className="w-full max-w-sm px-4">
      <div className="bg-white rounded-xl shadow-md p-6 space-y-6 border border-gray-200">
        <h2 className="text-xl font-semibold text-center text-gray-800">Login</h2>
        <form onSubmit={handleLogin} className="space-y-4">
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700">Email</label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            />
          </div>
          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700">Password</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            />
          </div>
          {error && <p className="text-sm text-red-600">{error}</p>}
          <button
            type="submit"
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-md"
          >
            Log In
          </button>
        </form>
      </div>
    </div>
  </div>
);


}

export default Login;
