// 📄 Dashboard.tsx
// This is the main dashboard page for the user.
// It shows their quota usage and their content request history.
// Each content request now includes a “View Details” link.

import React from "react";
import { useContentRequests, useUsageStats } from "../hooks/useDashboard";
import { formatDistanceToNow } from "date-fns";
import { Link } from "react-router-dom"; // 🔗 Needed for navigation links

const Dashboard: React.FC = () => {
  // 📦 Load the user's list of content requests (threads/articles they've submitted)
  const {
    data: requests = [],
    isLoading: loadingRequests,
    isError: errorRequests,
  } = useContentRequests();

  // 📊 Load the user's current quota usage
  const {
    data: usage = null,
    isLoading: loadingUsage,
    isError: errorUsage,
  } = useUsageStats();

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold">📊 Dashboard</h1>

      {/* --- QUOTA USAGE CARD --- */}
      <div className="bg-white shadow rounded-lg p-4 border">
        <h2 className="text-lg font-semibold mb-2">Quota Usage</h2>
        {loadingUsage ? (
          <p>Loading usage stats...</p>
        ) : errorUsage ? (
          <p className="text-red-500">Failed to load usage stats.</p>
        ) : usage ? (
          <div className="text-sm">
            <p>
              Used today:{" "}
              <span className="font-medium">
                {usage.api_quota_used_today ?? 0}
              </span>{" "}
              / {usage.api_quota_daily}
            </p>
            <p>
              Quota resets:{" "}
              <span className="text-gray-600">
                {usage.quota_reset_date ?? "N/A"}
              </span>
            </p>
          </div>
        ) : null}
      </div>

      {/* --- USER REQUEST HISTORY --- */}
      <div className="bg-white shadow rounded-lg p-4 border">
        <h2 className="text-lg font-semibold mb-2">Your Content Requests</h2>
        {loadingRequests ? (
          <p>Loading requests...</p>
        ) : errorRequests ? (
          <p className="text-red-500">Failed to load content requests.</p>
        ) : requests.length > 0 ? (
          <ul className="divide-y divide-gray-200 text-sm">
            {requests.map((req: any) => (
              <li key={req.id} className="py-3">
                <div className="flex justify-between items-start">
                  {/* 📝 Request summary: Topic, Status, Platform */}
                  <div>
                    <p className="font-medium">{req.original_topic}</p>
                    <p className="text-gray-500 text-xs">
                      Status: {req.status} • Platform: {req.platform}
                    </p>
                    {/* 🔗 View Details button (new) */}
                    <Link
                      to={`/requests/${req.id}`}
                      className="text-blue-600 hover:underline text-xs mt-1 inline-block"
                    >
                      View Details →
                    </Link>
                  </div>
                  {/* ⏱️ Timestamp showing how long ago it was created */}
                  <p className="text-xs text-gray-400">
                    {formatDistanceToNow(new Date(req.created_at), {
                      addSuffix: true,
                    })}
                  </p>
                </div>
              </li>
            ))}
          </ul>
        ) : (
          <p>No requests submitted yet.</p>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
