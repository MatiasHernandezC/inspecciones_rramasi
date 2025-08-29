import { apiFetch } from "./apiClient";
const BASE = "/api/proyectos";

export const ProyectosAPI = {
  // GET /api/proyectos?cliente_id=123
  listarPorCliente: (cliente_id) => apiFetch(`${BASE}?cliente_id=${encodeURIComponent(cliente_id)}`),
};
