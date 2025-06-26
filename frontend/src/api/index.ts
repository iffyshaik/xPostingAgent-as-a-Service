import axios from "axios";

const api = axios.create({
  baseURL: "/",
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// ✅ ADD THIS
export const submitTopic = async (payload: any) => {
  const response = await api.post("/content/requests", payload);
  return response.data;
};

export const fetchContentRequests = async () => {
  const response = await api.get("/content/requests");
  if (!Array.isArray(response.data)) throw new Error("Invalid response");
  return response.data;
};

export const fetchUsageStats = async () => {
  const response = await api.get("/users/usage-stats");
  if (!response.data?.success) throw new Error("Stats fetch failed");
  return response.data.data;
};

// 📄 fetchRequestDetail — get full detail for a content request by ID
export const fetchRequestDetail = async (requestId: string) => {
  const response = await api.get(`/content/requests/${requestId}`);
  return response.data.data; // We return only the "data" portion
};






// ✅ Needed for Login.tsx or other default imports
export default api;


