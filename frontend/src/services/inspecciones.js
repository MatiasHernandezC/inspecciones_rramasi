import { apiFetch } from "./apiClient";

export const InspeccionesAPI = {
  listar: (q="") => apiFetch(`/inspecciones?q=${encodeURIComponent(q)}`),
  crear: (payload) => apiFetch(`/inspecciones`, { method: "POST", body: JSON.stringify(payload) }),
  obtener: (id) => apiFetch(`/inspecciones/${id}`),
  actualizar: (id, payload) => apiFetch(`/inspecciones/${id}`, { method: "PATCH", body: JSON.stringify(payload) }),
  generarInforme: (id) => apiFetch(`/inspecciones/${id}/generar-informe`, { method: "POST" }),
  subirImagenes: (id, files) => {
    const fd = new FormData();
    files.forEach(f => fd.append("files", f));
    const base = process.env.REACT_APP_API_URL || "http://localhost:8080";
    return fetch(`${base}/inspecciones/${id}/imagenes`, {
      method: "POST",
      body: fd,
      credentials: "include",
    }).then(r => { if (!r.ok) throw new Error("Upload failed"); return r.json(); });
  }
}
