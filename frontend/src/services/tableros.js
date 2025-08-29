import { apiFetch } from "./apiClient";

const BASE = "/api/tableros";

export const TablerosAPI = {
  // GET /api/tableros?proyecto=ID
  listarPorProyecto: (proyecto) => apiFetch(`${BASE}?proyecto=${encodeURIComponent(proyecto)}`),
  listar: ({ skip = 0, limit = 100 } = {}) => apiFetch(`${BASE}/?skip=${skip}&limit=${limit}`),
  obtener: (id) => apiFetch(`${BASE}/${id}`),
  crear: (payload) => apiFetch(`${BASE}/`, { method: "POST", body: JSON.stringify(payload) }),
  actualizar: (id, payload) => apiFetch(`${BASE}/${id}`, { method: "PUT", body: JSON.stringify(payload) }),
  eliminar: (id) => apiFetch(`${BASE}/${id}`, { method: "DELETE" }),
};

