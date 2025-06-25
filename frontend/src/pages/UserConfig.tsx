// UserConfig.tsx
// This page will let users configure their writing persona, tone, style, language, and preferences.

import Layout from "../components/Layout";

function UserConfig() {
  return (
    <Layout>
      <h1 className="text-2xl font-bold">⚙️ User Configuration</h1>
      <p className="mt-4">
        This page will allow users to view and update their writing preferences,
        such as persona, tone, style, language, and default platform.
      </p>
    </Layout>
  );
}

export default UserConfig;
