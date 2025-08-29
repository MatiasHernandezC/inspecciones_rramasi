import React from "react";
import { useNavigate } from "react-router-dom";

export default function DashboardPage(){
  const nav = useNavigate();
  return (
    <>
      <h2 style={{fontSize:22, fontWeight:800, marginTop:10}}>Acciones</h2>

      <section className="section">
        <h3 className="sectionTitle">Nueva Inspecci�n</h3>
        <div className="row">
          <button className="btn" onClick={()=>nav("/inspecciones/nueva")}>Nueva Inspecci�n</button>
          <div className="spacer"/>
        </div>
      </section>

      <section className="section">
        <h3 className="sectionTitle">Revisar Proyectos</h3>
        <div className="row">
          <div className="spacer"/>
          <button className="btn" onClick={()=>nav("/inspecciones")}>Ir a revisar proyectos</button>
        </div>
      </section>

      <section className="section">
        <h3 className="sectionTitle">Administrar im�genes</h3>
        <div className="row">
          <button className="btn ghost" onClick={()=>nav("/imagenes")}>Tomar Im�genes</button>
          <button className="btn secondary" onClick={()=>nav("/imagenes")}>Subir Im�genes</button>
          <button className="btn" onClick={()=>nav("/imagenes")}>Adjuntar a Proyecto</button>
        </div>
      </section>
    </>
  );
}
