// App.tsx
// This is the main route manager for the frontend app.
// It defines what page to show when a user visits a certain URL.

import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import SubmitTopic from "./pages/SubmitTopic";
import UserConfig from "./pages/UserConfig";
import ScheduledPosts from "./pages/ScheduledPosts";
import RequestDetail from "./pages/RequestDetail";

import ProtectedRoute from "./components/ProtectedRoute";
import { AuthProvider } from "./hooks/AuthProvider";
import Layout from "./components/Layout";

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          {/* Public route: login */}
          <Route path="/login" element={<Login />} />

          {/* Protected route: dashboard */}
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Layout>
                  <Dashboard />
                </Layout>
              </ProtectedRoute>
            }
          />

          {/* Protected route: topic submission */}
          <Route
            path="/submit"
            element={
              <ProtectedRoute>
                <Layout>
                  <SubmitTopic />
                </Layout>
              </ProtectedRoute>
            }
          />

          {/* Protected route: user configuration */}
          <Route
            path="/config"
            element={
              <ProtectedRoute>
                <Layout>
                  <UserConfig />
                </Layout>
              </ProtectedRoute>
            }
          />

          {/* Protected route: scheduled posts */}
          <Route 
            path="/schedule"
            element={
              <ProtectedRoute>
                <Layout>
                  <ScheduledPosts />
                </Layout>
              </ProtectedRoute>
            }
          />

          {/* ✅ NEW: Request detail view */}
          < Route path="/requests/:id" element={<ProtectedRoute> <Layout> <RequestDetail /> </Layout> </ProtectedRoute>} />

          {/* Default fallback: redirect to login */}
          <Route path="*" element={<Login />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
