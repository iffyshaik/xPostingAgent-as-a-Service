// Dashboard.tsx
// Displays basic info inside the main layout. This is the user's home after login.

import Layout from "../components/Layout";

function Dashboard() {
  return (
    <Layout>
      <h1 className="text-2xl font-bold">📊 Dashboard</h1>
      <p className="mt-4">Welcome! This is your dashboard view.</p>
    </Layout>
  );
}

export default Dashboard;
