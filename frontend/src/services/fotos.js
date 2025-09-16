import { apiFetch } from "./apiClient";

const BASE = "/api/fotos";

export const FotosAPI = {
  listar: async (params = {}) => {
    const query = new URLSearchParams(params).toString();
    return apiFetch(`${BASE}/?${query}`);
  },

  listarPorInspeccion: async (id_inspeccion) => {
    return apiFetch(`${BASE}/?id_inspeccion=${id_inspeccion}`);
  },

  crear: async ({
    file,
    id_cliente,
    id_proyecto,
    id_tablero,
    id_inspeccion,
    id_informe,
    id_integrador,
    id_item,
    fecha_captura,
  }) => {
    const formData = new FormData();
    formData.append("file", file);
    if (id_cliente) formData.append("id_cliente", id_cliente);
    if (id_proyecto) formData.append("id_proyecto", id_proyecto);
    if (id_tablero) formData.append("id_tablero", id_tablero);
    if (id_inspeccion) formData.append("id_inspeccion", id_inspeccion);
    if (id_informe) formData.append("id_informe", id_informe);
    if (id_integrador) formData.append("id_integrador", id_integrador);
    if (id_item) formData.append("id_item", id_item);
    if (fecha_captura) formData.append("fecha_captura", fecha_captura);

    console.log("Subiendo foto con FormData:", formData);
    for (let [key, value] of formData.entries()) {
      console.log(key, value);
    }
    return apiFetch(`${BASE}/upload`, { method: "POST", body: formData, headers: {} });
  },

  obtener: (id) => apiFetch(`${BASE}/${id}`),

  eliminar: (id) => apiFetch(`${BASE}/${id}`, { method: "DELETE" }),
};
