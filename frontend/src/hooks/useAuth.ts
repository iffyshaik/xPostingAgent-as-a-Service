// useAuth.ts
// This custom React hook manages authentication state.
// It checks if the user is logged in (based on the presence of a JWT token).

import { useEffect, useState } from "react";

function useAuth() {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);

  useEffect(() => {
    // Check for token in localStorage
    const token = localStorage.getItem("token");
    setIsAuthenticated(!!token); // true if token exists, false otherwise
  }, []);

  return { isAuthenticated };
}

export default useAuth;
