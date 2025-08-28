const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:8080";

export async function apiFetch(path, opts) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json", ...(opts?.headers || {}) },
    credentials: "include",
    ...opts,
  });
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  const isJson = res.headers.get("content-type")?.includes("application/json");
  return isJson ? res.json() : res.text();
}
