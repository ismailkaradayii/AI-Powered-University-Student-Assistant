/**
 * WBS 3.1 & 3.2 - Frontend API Client & JWT Session Helper
 * Owner: Rabia Basan (20230147)
 */

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000/api";

export function getAccessToken() {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("swe488_access_token");
}

export function getStoredUser() {
  if (typeof window === "undefined") return null;
  const raw = localStorage.getItem("swe488_user");
  return raw ? JSON.parse(raw) : null;
}

export function setAuthSession(accessToken, refreshToken, user) {
  if (typeof window === "undefined") return;
  localStorage.setItem("swe488_access_token", accessToken);
  localStorage.setItem("swe488_refresh_token", refreshToken);
  localStorage.setItem("swe488_user", JSON.stringify(user));
}

export function clearAuthSession() {
  if (typeof window === "undefined") return;
  localStorage.removeItem("swe488_access_token");
  localStorage.removeItem("swe488_refresh_token");
  localStorage.removeItem("swe488_user");
}

export async function apiRequest(endpoint, options = {}) {
  const token = getAccessToken();
  const headers = {
    "Content-Type": "application/json",
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...(options.headers || {}),
  };

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    const error = new Error(
      data.detail || "An error occurred while communicating with the server."
    );
    error.status = response.status;
    error.payload = data;
    throw error;
  }
  return data;
}
