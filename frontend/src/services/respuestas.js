import { apiFetch } from "./apiClient";

export const RespuestasAPI = {
  bulkUpsert: (id_inspeccion, respuestas) =>
    apiFetch(`/api/inspecciones/${id_inspeccion}/respuestas-bulk`, {
      method: "POST",
      body: JSON.stringify({ respuestas }),
    }),
};

