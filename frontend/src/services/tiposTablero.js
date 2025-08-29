import { apiFetch } from "./apiClient";

const BASE = "/api/tipos-tablero";

export const TiposTableroAPI = {
  listar: ({ skip = 0, limit = 100 } = {}) => apiFetch(`${BASE}/?skip=${skip}&limit=${limit}`),
  obtener: (id) => apiFetch(`${BASE}/${id}`),
};

