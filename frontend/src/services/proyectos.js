import { apiFetch } from "./apiClient";
const BASE = "/api/proyectos";

export const ProyectosAPI = {
  // GET /api/proyectos?cliente=123
  listarPorCliente: (cliente) => apiFetch(`${BASE}?cliente=${encodeURIComponent(cliente)}`),
  // GET /api/proyectos
  listar: ({ skip = 0, limit = 100 } = {}) => apiFetch(`${BASE}/?skip=${skip}&limit=${limit}`),
  obtener: (id) => apiFetch(`${BASE}/${id}`),
};
