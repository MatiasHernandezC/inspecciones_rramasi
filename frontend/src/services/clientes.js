// src/services/clientes.js
import { apiFetch } from "./apiClient";

// Base en FastAPI: /api/clientes/
const BASE = "/api/clientes";

export const ClientesAPI = {
  // GET /api/clientes/?skip=0&limit=100
  listar: ({ skip = 0, limit = 100 } = {}) =>
    apiFetch(`${BASE}/?skip=${encodeURIComponent(skip)}&limit=${encodeURIComponent(limit)}`),

  // GET /api/clientes/{id}
  obtener: (id_cliente) => apiFetch(`${BASE}/${id_cliente}`),

  // POST /api/clientes/
  crear: (payload) =>
    apiFetch(`${BASE}/`, {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  // PUT /api/clientes/{id}
  actualizar: (id_cliente, payload) =>
    apiFetch(`${BASE}/${id_cliente}`, {
      method: "PUT",
      body: JSON.stringify(payload),
    }),

  // DELETE /api/clientes/{id}
  eliminar: (id_cliente) =>
    apiFetch(`${BASE}/${id_cliente}`, {
      method: "DELETE",
    }),
};
