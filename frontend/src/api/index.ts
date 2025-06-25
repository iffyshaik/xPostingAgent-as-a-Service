// src/api/index.ts
/**
 * Axios instance configured with base URL and JWT token handling.
 * Automatically includes Bearer token from localStorage on every request.
 */

import axios from "axios";

// You can later move this to an .env file
const API_BASE_URL = "http://localhost:8000"; // FastAPI backend

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Add token to every request
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export default apiClient;
