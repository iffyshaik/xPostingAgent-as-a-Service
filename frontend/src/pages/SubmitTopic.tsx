// SubmitTopic.tsx
// This page will allow the user to enter a topic and configure content generation options.

import Layout from "../components/Layout";

function SubmitTopic() {
  return (
    <Layout>
      <h1 className="text-2xl font-bold">📝 Submit a New Topic</h1>
      <p className="mt-4">
        This page will let users input a topic, choose a content type and platform,
        and optionally customise tone, style, and persona.
      </p>
    </Layout>
  );
}

export default SubmitTopic;
