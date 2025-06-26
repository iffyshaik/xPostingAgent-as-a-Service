// 📄 useRequestDetail.ts
// This hook fetches full details for a content request by ID.
// It returns loading, error, and the request data for rendering the detail view.

import { useEffect, useState } from "react";
import api from "../api";

export const useRequestDetail = (requestId: string) => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await api.get(`/content/requests/${requestId}`);
        setData(response.data);
      } catch (err) {
        setError("Failed to load request details.");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [requestId]);

  return { data, loading, error };
};
