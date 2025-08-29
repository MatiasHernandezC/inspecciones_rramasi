import { apiFetch } from "./apiClient";

export const ChecklistAPI = {
  // GET /api/get_checklist?tablero=ID
  resolverPorTablero: (tablero) => apiFetch(`/api/get_checklist?tablero=${encodeURIComponent(tablero)}`),
  // GET /api/get_checklist?tipo=ID
  resolverPorTipo: (tipo) => apiFetch(`/api/get_checklist?tipo=${encodeURIComponent(tipo)}`),
};
