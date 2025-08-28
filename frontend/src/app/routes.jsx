import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import DashboardPage from "../pages/Dashboard/DashboardPage";
import NuevaInspeccionPage from "../pages/Inspecciones/Nueva/NuevaInspeccionPage";
import InspeccionesPage from "../pages/Inspecciones/Listado/InspeccionesPage";
import GestorImagenesPage from "../pages/Imagenes/GestorImagenesPage";

export default function AppRoutes(){
  return (
    <Routes>
      <Route path="/" element={<DashboardPage />} />
      <Route path="/inspecciones" element={<InspeccionesPage />} />
      <Route path="/inspecciones/nueva" element={<NuevaInspeccionPage />} />
      <Route path="/imagenes" element={<GestorImagenesPage />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
