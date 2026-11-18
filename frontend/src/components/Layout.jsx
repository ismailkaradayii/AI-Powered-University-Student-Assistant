/**
 * WBS 3.1 - University Portal Layout & Responsive Navigation Component
 * Owner: Rabia Basan (20230147)
 */
import Link from "next/link";
import { useRouter } from "next/router";
import { clearAuthSession } from "../lib/api";

export default function Layout({ user, children }) {
  const router = useRouter();

  const handleLogout = () => {
    clearAuthSession();
    router.push("/pages/login");
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-50">
      <header className="bg-slate-900 text-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <span className="bg-red-700 text-white font-bold px-2.5 py-1 rounded text-sm">
              SWE488
            </span>
            <span className="font-semibold text-lg tracking-tight">
              AI-Powered University Student Assistant
            </span>
          </div>

          {user && (
            <nav className="flex items-center space-x-6 text-sm">
              <Link
                href="/pages/dashboard"
                className="hover:text-red-400 transition-colors"
              >
                Student Dashboard
              </Link>
              {user.is_staff && (
                <Link
                  href="/pages/admin"
                  className="bg-amber-600 hover:bg-amber-500 px-3 py-1.5 rounded font-medium transition-colors"
                >
                  Admin Panel
                </Link>
              )}
              <span className="text-slate-300 hidden sm:inline">
                {user.full_name} ({user.student_number})
              </span>
              <button
                onClick={handleLogout}
                className="text-red-300 hover:text-white font-medium"
              >
                Logout
              </button>
            </nav>
          )}
        </div>
      </header>

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>

      <footer className="bg-white border-t border-slate-200 py-4 text-center text-xs text-slate-500">
        SWE488 Software Implementation Project &bull; AI-Powered University Student Assistant (2026)
      </footer>
    </div>
  );
}
