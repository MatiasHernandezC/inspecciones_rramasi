import { apiFetch } from "./apiClient";

const BASE = "/api/fotos";

export const FotosAPI = {
  listarPorInspeccion: (id_inspeccion) => apiFetch(`${BASE}/?inspeccion=${encodeURIComponent(id_inspeccion)}`),
  crear: (payload) => apiFetch(`${BASE}/`, { method: "POST", body: JSON.stringify(payload) }),
};
