import { apiFetch } from "./apiClient";

const BASE = "/api/fotos";

export const FotosAPI = {
  crear: (payload) => apiFetch(`${BASE}/`, { method: "POST", body: JSON.stringify(payload) }),
};

