// ScheduledPosts.tsx
// This page will display all scheduled posts and allow users to reschedule or delete them.

// import Layout from "../components/Layout";

// function ScheduledPosts() {
//   return (
//     <>
//       <h1 className="text-2xl font-bold">📅 Scheduled Posts</h1>
//       <p className="mt-4">
//         This page will show upcoming scheduled content. Users will be able to reschedule
//         or cancel posts directly from here.
//       </p>
//     </>
//   );
// }

// export default ScheduledPosts;


// ScheduledPosts.tsx
// This page displays all scheduled posts and highlights deleted ones.

import { useEffect, useState } from "react";
import Layout from "../components/Layout";

interface ScheduledPost {
  id: number;
  content_type: string;
  generated_content: string;
  scheduled_for: string;
  deleted_at: string | null;
  status: string;
  platform: string;
}

function ScheduledPosts() {
  const [posts, setPosts] = useState<ScheduledPost[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const fetchPosts = () => {
    fetch("/content/queue/scheduled", {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
        "Content-Type": "application/json"
      }
    })
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch scheduled posts");
        return res.json();
      })
      .then((data) => {
        setPosts(data.data || []);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setError("Unable to load scheduled posts.");
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchPosts();
  }, []);

  const handleDelete = async (id: number) => {
    const res = await fetch(`/content/queue/${id}`, {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`
      }
    });
    if (res.ok) fetchPosts();
    else alert("Failed to delete post.");
  };

  const handleManualPost = async (id: number) => {
    const res = await fetch(`/content/queue/${id}/post`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`
      }
    });
    if (res.ok) fetchPosts();
    else alert("Failed to post content.");
  };

  return (
    <>
      <div className="max-w-3xl mx-auto py-6 px-4">
        <h1 className="text-2xl font-bold">📅 Scheduled Posts</h1>
        <p className="mt-2 text-gray-600">
          View, manually post, or delete scheduled content.
        </p>

        {loading && <p className="mt-6">Loading scheduled posts...</p>}
        {error && <p className="mt-6 text-red-600">{error}</p>}

        {!loading && posts.length === 0 && (
          <p className="mt-6 text-gray-500">No scheduled posts found.</p>
        )}

        <ul className="mt-6 space-y-4">
          {posts.map((post) => (
            <li
              key={post.id}
              className={`p-4 rounded-md border ${
                post.deleted_at ? "bg-gray-100 text-gray-500" : "bg-white"
              }`}
            >
              <div className="flex justify-between items-center">
                <div>
                  <strong>{post.content_type.toUpperCase()}</strong> —{" "}
                  {new Date(post.scheduled_for).toLocaleString()}
                  {post.deleted_at && (
                    <span className="ml-2 text-sm text-red-500 font-semibold">
                      (Deleted)
                    </span>
                  )}
                </div>
                <div className="space-x-2">
                  {!post.deleted_at && (
                    <>
                      <button
                        className="text-sm text-blue-600 hover:underline"
                        onClick={() => handleManualPost(post.id)}
                      >
                        Post Now
                      </button>
                      <button
                        className="text-sm text-red-600 hover:underline"
                        onClick={() => handleDelete(post.id)}
                      >
                        Delete
                      </button>
                    </>
                  )}
                </div>
              </div>
              <p className="mt-2 text-sm italic">
                {post.generated_content.slice(0, 140)}...
              </p>
            </li>
          ))}
        </ul>
      </div>
    </>
  );
}

export default ScheduledPosts;
