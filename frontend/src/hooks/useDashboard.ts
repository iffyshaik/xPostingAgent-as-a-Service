// frontend/src/hooks/useDashboard.ts
import { useQuery } from "@tanstack/react-query";
import { fetchContentRequests, fetchUsageStats } from "../api/index";

export const useContentRequests = () => {
  return useQuery({
    queryKey: ["contentRequests"],
    queryFn: fetchContentRequests,
  });
};

export const useUsageStats = () => {
  return useQuery({
    queryKey: ["usageStats"],
    queryFn: fetchUsageStats,
  });
};
