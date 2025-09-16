// src/pages/Dashboard.jsx
import React from "react";
import { useNavigate } from "react-router-dom";

export default function DashboardPage() {
  const nav = useNavigate();
  return (
    <>
      <h2 style={{ fontSize: 22, fontWeight: 800, marginTop: 10 }}>Acciones</h2>
      <section className="section">
        <h3 className="sectionTitle">Nueva Inspección</h3>
        <div className="row">
          <button className="btn" onClick={() => nav("/inspecciones/nueva")}>
            Nueva Inspección
          </button>
          <div className="spacer" />
        </div>
      </section>

      <section className="section">
        <h3 className="sectionTitle">Revisar Proyectos</h3>
        <div className="row">
          <button className="btn" onClick={() => nav("/proyectos")}>Ir a revisar proyectos</button>
          <div className="spacer" />
        </div>
      </section>

      <section className="section">
        <h3 className="sectionTitle">Administrar imágenes</h3>
        <div className="row">
          <button className="btn ghost" onClick={() => nav("/imagenes")}>
            Tomar Imágenes
          </button>
          <button className="btn secondary" onClick={() => nav("/imagenes")}>
            Subir Imágenes
          </button>
          <button className="btn" onClick={() => nav("/imagenes")}>
            Adjuntar a Proyecto
          </button>
        </div>
      </section>
      <section className="section">
        <h3 className="sectionTitle">Clientes</h3>
        <div className="row">
          <button className="btn" onClick={() => nav("/clientes")}>
            Ver Clientes
          </button>
          <button className="btn secondary" onClick={() => nav("/clientes/nuevo")}>
            Nuevo Cliente
          </button>
          <div className="spacer" />
        </div>
      </section>
    </>
  );
}
