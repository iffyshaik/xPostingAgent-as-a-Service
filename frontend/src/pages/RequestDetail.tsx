// 📄 RequestDetail.tsx
// This page displays full details of a content request: topics, sources, summary, and content.
// It also includes actions for approving or scheduling the content.

import { useParams, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import { fetchRequestDetail } from "../api";
import { format } from "date-fns";
import api from "../api";

const RequestDetail = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const [data, setData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [scheduledFor, setScheduledFor] = useState("");

  useEffect(() => {
    fetchRequestDetail(id!)
      .then(setData)
      .catch(() => setError("Failed to load request."))
      .finally(() => setLoading(false));
  }, [id]);

  const handleApprove = async () => {
    if (!data?.content?.id) {
      alert("No content ID found to approve.");
      return;
    }

    try {
      console.log("Request detail:", data);
      await api.put(`/content/queue/${data.content.id}/approve`);
      alert("Content approved!");
      navigate("/dashboard");
    } catch {
      alert("Failed to approve content.");
    }
  };

  const handleSchedule = async () => {
    try {
      await api.put(`/content/queue/${data.content.id}/schedule`, {
        scheduled_for: scheduledFor,
      });
      alert("Content scheduled!");
      navigate("/dashboard");
    } catch {
      alert("Failed to schedule content.");
    }
  };

  if (loading) return <div className="p-4">Loading...</div>;
  if (error) return <div className="p-4 text-red-500">{error}</div>;

  const { request, sources, summary, content } = data;

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold">Request Details</h1>

      <section className="border p-4 rounded bg-white">
        <h2 className="font-semibold">Metadata</h2>
        <p><strong>Original Topic:</strong> {request.original_topic}</p>
        <p><strong>Refined Topic:</strong> {request.content_topic || "N/A"}</p>
        <p><strong>Type:</strong> {request.content_type}</p>
        <p><strong>Status:</strong> {request.status}</p>
        <p><strong>Platform:</strong> {request.platform}</p>
        <p><strong>Created:</strong> {format(new Date(request.created_at), "PPPpp")}</p>
      </section>

      <section className="border p-4 rounded bg-white">
        <h2 className="font-semibold mb-2">Verified Sources</h2>
        {sources.length === 0 && <p>No sources found.</p>}
        {sources.map((src: any, idx: number) => (
          <div key={idx} className="mb-2 border-b pb-2">
            <a href={src.url} className="text-blue-600 underline" target="_blank" rel="noreferrer">
              {src.title || src.url}
            </a>
            <p><strong>Type:</strong> {src.source_type} | <strong>Score:</strong> {src.relevance_score}</p>
            <p className="text-sm italic">{src.summary}</p>
          </div>
        ))}
      </section>

      <section className="border p-4 rounded bg-white">
        <h2 className="font-semibold mb-2">Summary</h2>
        <p>{summary.combined_summary || "No summary available."}</p>
        <ul className="list-disc pl-6 mt-2">
          {summary.key_points?.map((point: string, idx: number) => (
            <li key={idx}>{point}</li>
          ))}
        </ul>
      </section>

      <section className="border p-4 rounded bg-white">
        <h2 className="font-semibold mb-2">Generated Content</h2>
        <pre className="whitespace-pre-wrap bg-gray-100 p-2 rounded text-sm">
          {content.generated_content || "No content yet."}
        </pre>
        <p className="mt-2"><strong>Status:</strong> {content.status}</p>

        {/* --- ACTION BUTTONS --- */}
        {content.status === "draft" && (
          <div className="mt-4 space-y-2">
            {/* Approve Button */}
            <button
              onClick={handleApprove}
              className="bg-green-600 text-white text-sm px-4 py-2 rounded hover:bg-green-700"
            >
              ✅ Approve Content
            </button>

            {/* Schedule Form */}
            <div className="mt-4">
              <label className="block text-sm font-medium mb-1">
                Schedule for later:
              </label>
              <input
                type="datetime-local"
                value={scheduledFor}
                onChange={(e) => setScheduledFor(e.target.value)}
                className="border px-2 py-1 rounded text-sm mr-2"
              />
              <button
                onClick={handleSchedule}
                className="bg-blue-600 text-white text-sm px-4 py-2 rounded hover:bg-blue-700"
              >
                🗕️ Schedule Post
              </button>
            </div>
          </div>
        )}
      </section>
    </div>
  );
};

export default RequestDetail;
