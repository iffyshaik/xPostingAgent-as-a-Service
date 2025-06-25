// Layout.tsx
// This component wraps each page in a consistent layout with a top navbar and logout button.

import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/AuthProvider";

type Props = {
  children: React.ReactNode;
};

const Layout = ({ children }: Props) => {
  const { logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      {/* Top navigation bar */}
      <nav className="bg-white shadow-md px-6 py-4 flex justify-between items-center">
        <div className="flex gap-6 font-semibold text-blue-600 text-sm">
            <Link to="/dashboard" className="hover:underline inline-block">
                Dashboard
            </Link>
            <Link to="/submit" className="hover:underline inline-block">
                Submit
            </Link>
            <Link to="/config" className="hover:underline inline-block">
                Config
            </Link>
            <Link to="/schedule" className="hover:underline inline-block">
                Schedule
            </Link>
        </div>

        <button
          onClick={handleLogout}
          className="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600 text-sm"
        >
          Logout
        </button>
      </nav>

      {/* Page content */}
      <main className="p-6">{children}</main>
    </div>
  );
};

export default Layout;
