import { apiFetch } from "./apiClient";

const BASE = "/api/integradores";

export const IntegradoresAPI = {
  listar: ({ skip = 0, limit = 100 } = {}) => apiFetch(`${BASE}/?skip=${skip}&limit=${limit}`),
  obtener: (id) => apiFetch(`${BASE}/${id}`),
  crear: (payload) => apiFetch(`${BASE}/`, { method: "POST", body: JSON.stringify(payload) }),
  actualizar: (id, payload) => apiFetch(`${BASE}/${id}`, { method: "PUT", body: JSON.stringify(payload) }),
  eliminar: (id) => apiFetch(`${BASE}/${id}`, { method: "DELETE" }),
};

