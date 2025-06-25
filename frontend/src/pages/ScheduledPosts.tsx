// ScheduledPosts.tsx
// This page will display all scheduled posts and allow users to reschedule or delete them.

import Layout from "../components/Layout";

function ScheduledPosts() {
  return (
    <Layout>
      <h1 className="text-2xl font-bold">📅 Scheduled Posts</h1>
      <p className="mt-4">
        This page will show upcoming scheduled content. Users will be able to reschedule
        or cancel posts directly from here.
      </p>
    </Layout>
  );
}

export default ScheduledPosts;
