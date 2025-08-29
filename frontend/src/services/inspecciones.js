import { apiFetch } from "./apiClient";

const BASE = "/api/inspecciones";
const PROYECTOS = "/api/proyectos";
const CLIENTES = "/api/clientes";

export const InspeccionesAPI = {
  // Lista básica, adaptada al shape {id, cliente, proyecto, fecha, estado}
  listar: async ({ skip = 0, limit = 100 } = {}) => {
    const ins = await apiFetch(`${BASE}/?skip=${skip}&limit=${limit}`);
    // Enriquecemos con nombre de proyecto/cliente (N+1 simple). Se puede optimizar con endpoint dedicado.
    const withMeta = await Promise.all(
      ins.map(async (i) => {
        try {
          const p = await apiFetch(`${PROYECTOS}/${i.id_proyecto}`);
          const c = await apiFetch(`${CLIENTES}/${p.id_cliente}`);
          return {
            id: i.id_inspeccion,
            cliente: c.nombre,
            proyecto: p.nombre,
            fecha: i.fecha_inspeccion || i.created_at,
            estado: i.estado || "draft",
          };
        } catch (_) {
          return {
            id: i.id_inspeccion,
            cliente: `#${i.id_proyecto}`,
            proyecto: `Proyecto ${i.id_proyecto}`,
            fecha: i.fecha_inspeccion || i.created_at,
            estado: i.estado || "draft",
          };
        }
      })
    );
    return withMeta;
  },
  crear: (payload) => apiFetch(`${BASE}/`, { method: "POST", body: JSON.stringify(payload) }),
  obtener: (id) => apiFetch(`${BASE}/${id}`),
  // Backend expone PUT para actualizar
  actualizar: (id, payload) => apiFetch(`${BASE}/${id}`, { method: "PUT", body: JSON.stringify(payload) }),
};
