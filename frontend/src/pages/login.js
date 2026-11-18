/**
 * WBS 3.2 - Student Secure Login Page (/pages/login)
 * Covers Test Case TC-01 (Valid Login -> JWT & Redirect to /pages/dashboard)
 * Covers Test Case TC-02 (Invalid Password -> HTTP 401 Red Informative Error Message)
 * Owner: Rabia Basan (20230147)
 */
import { useState } from "react";
import { useRouter } from "next/router";
import { apiRequest, setAuthSession } from "../lib/api";

export default function LoginPage() {
  const router = useRouter();
  const [studentNumber, setStudentNumber] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage("");
    setLoading(true);

    try {
      const data = await apiRequest("/auth/login/", {
        method: "POST",
        body: JSON.stringify({
          student_number: studentNumber,
          password: password,
        }),
      });
      setAuthSession(data.access, data.refresh, data.user);
      router.push("/pages/dashboard");
    } catch (err) {
      setErrorMessage(
        err.message ||
          "HTTP 401 Unauthorized: Invalid student number or password."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-100 px-4">
      <div className="max-w-md w-full bg-white rounded-xl shadow-lg p-8 border border-slate-200">
        <div className="text-center mb-6">
          <span className="inline-block bg-red-700 text-white text-xs font-bold px-3 py-1 rounded-full mb-2">
            NEAR EAST UNIVERSITY &bull; SWE488
          </span>
          <h1 className="text-2xl font-bold text-slate-900">
            Student Assistant Portal
          </h1>
          <p className="text-sm text-slate-500 mt-1">
            Sign in with your Student Number and Password
          </p>
        </div>

        {errorMessage && (
          <div
            role="alert"
            data-testid="login-error-alert"
            className="mb-4 p-3.5 rounded-lg bg-red-50 border border-red-400 text-red-700 text-sm font-medium"
          >
            {errorMessage}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">
              Student Number
            </label>
            <input
              type="text"
              required
              placeholder="e.g. 20220236"
              value={studentNumber}
              onChange={(e) => setStudentNumber(e.target.value)}
              className="w-full px-3.5 py-2.5 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-600 text-sm"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">
              Password
            </label>
            <input
              type="password"
              required
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-3.5 py-2.5 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-600 text-sm"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-red-700 hover:bg-red-800 disabled:opacity-50 text-white font-semibold py-2.5 rounded-lg transition-colors text-sm"
          >
            {loading ? "Signing in..." : "Login"}
          </button>
        </form>

        <div className="mt-6 pt-4 border-t border-slate-100 text-xs text-slate-500">
          <p className="font-semibold text-slate-700 mb-1">Demo Credentials (Seeded):</p>
          <p>Student / Admin: <code className="bg-slate-100 px-1 py-0.5 rounded">20220236</code> / <code className="bg-slate-100 px-1 py-0.5 rounded">password123</code></p>
        </div>
      </div>
    </div>
  );
}
