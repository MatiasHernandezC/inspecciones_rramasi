// src/services/proyectos.js
import { apiFetch } from "./apiClient";

const BASE = "/api/proyectos";

export const ProyectosAPI = {
  listar: ({ skip = 0, limit = 100, cliente = null } = {}) =>
    apiFetch(`${BASE}/?skip=${skip}&limit=${limit}${cliente ? `&cliente=${cliente}` : ""}`),
  
  listarPorCliente: (clienteId) =>
    apiFetch(`${BASE}/?cliente=${clienteId}`),

  listarPorProyecto: (proyectoId) =>
    apiFetch(`${BASE}/?proyecto=${proyectoId}`),

  obtener: (id) => apiFetch(`${BASE}/${id}`),
  
  crear: (payload) =>
    apiFetch(`${BASE}/`, { method: "POST", body: JSON.stringify(payload) }),
  
  actualizar: (id, payload) =>
    apiFetch(`${BASE}/${id}`, { method: "PUT", body: JSON.stringify(payload) }),
  
  eliminar: (id) =>
    apiFetch(`${BASE}/${id}`, { method: "DELETE" }),
};
