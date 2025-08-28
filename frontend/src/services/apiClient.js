// src/services/apiClient.js
const API_BASE =
  (typeof import.meta !== "undefined" && import.meta.env && import.meta.env.VITE_API_URL) ||
  process.env.REACT_APP_API_URL ||
  "http://localhost:8000";

function joinUrl(base, path) {
  if (!base.endsWith("/") && !path.startsWith("/")) return `${base}/${path}`;
  if (base.endsWith("/") && path.startsWith("/")) return `${base}${path.slice(1)}`;
  return `${base}${path}`;
}

export async function apiFetch(path, opts) {
  const url = joinUrl(API_BASE, path);
  const res = await fetch(url, {
    headers: { "Content-Type": "application/json", ...(opts?.headers || {}) },
    credentials: "include",
    ...opts,
  });
  if (!res.ok) {
    // intentar extraer mensaje útil del backend
    let msg = `${res.status} ${res.statusText}`;
    try {
      const data = await res.json();
      if (data?.detail) msg = Array.isArray(data.detail) ? data.detail.map(d => d.msg).join(", ") : data.detail;
    } catch (_) {}
    throw new Error(msg);
  }
  const isJson = res.headers.get("content-type")?.includes("application/json");
  return isJson ? res.json() : res.text();
}