// ProtectedRoute.tsx
// A route wrapper that ensures only authenticated users can access certain pages.

import { Navigate } from "react-router-dom";
import { useAuth } from "../hooks/AuthProvider";

type Props = {
  children: React.ReactNode;
};

const ProtectedRoute = ({ children }: Props) => {
  const { isAuthenticated } = useAuth();

  // Prevent infinite redirect loops
  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }

  return <>{children}</>;
};

export default ProtectedRoute;
