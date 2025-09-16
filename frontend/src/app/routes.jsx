import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import DashboardPage from "../pages/Dashboard/DashboardPage";
import NuevaInspeccionPage from "../pages/Inspecciones/Nueva/NuevaInspeccionPage";
import EditarInspeccionPage from "../pages/Inspecciones/Detalle/EditarInspeccionPage";
import InspeccionesPage from "../pages/Inspecciones/Listado/InspeccionesPage";
import GestorImagenesPage from "../pages/Imagenes/GestorImagenesPage";
import ClientesPage from "../pages/Clientes/ClientesPage";
import ClientesFormPage from "../pages/Clientes/ClientesFormPage";
import ProyectosPage from "../pages/Proyectos/ProyectosPage";
import ProyectosFormPage from "../pages/Proyectos/ProyectosFormPage";

export default function AppRoutes(){
  return (
    <Routes>
      <Route path="/" element={<DashboardPage />} />
      <Route path="/inspecciones" element={<InspeccionesPage />} />
      <Route path="/inspecciones/:id" element={<EditarInspeccionPage />} />
      <Route path="/inspecciones/nueva" element={<NuevaInspeccionPage />} />
      <Route path="/imagenes" element={<GestorImagenesPage />} />
      <Route path="/clientes" element={<ClientesPage />} />
      <Route path="/clientes/nuevo" element={<ClientesFormPage />} />
      <Route path="/clientes/editar/:id" element={<ClientesFormPage />} />
      <Route path="/proyectos" element={<ProyectosPage />} />
      <Route path="/proyectos/nuevo" element={<ProyectosFormPage />} />
      <Route path="/proyectos/:id/editar" element={<ProyectosFormPage />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
