import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function DashboardPage(){
  const nav = useNavigate();
  const [open, setOpen] = useState(false);
  const planillas = [
    { id: "base", label: "Planilla Base" },
    { id: "electrica", label: "Instalación Eléctrica" },
    { id: "seguridad", label: "Seguridad Industrial" },
  ];
  return (
    <>
      <h2 style={{fontSize:22, fontWeight:800, marginTop:10}}>Acciones</h2>

      <section className="section">
        <h3 className="sectionTitle">Nueva Inspección</h3>
        <div className="row">
          <button className="btn" onClick={()=>nav("/inspecciones/nueva?tipo=base")}>Planilla Base</button>
          <div className="spacer"/>
          <div className="dropdown">
            <button className="btn secondary" onClick={()=>setOpen(v=>!v)}>Escoger Planilla ▾</button>
            {open && (
              <div className="dropdownList" role="listbox">
                {planillas.map(p=> (
                  <div key={p.id} className="dropdownItem" onClick={()=>{ setOpen(false); nav(`/inspecciones/nueva?tipo=${p.id}`); }}>
                    {p.label}
                  </div>
                ))}
              </div>
            )}
          </div>
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
        <h3 className="sectionTitle">Administrar imágenes</h3>
        <div className="row">
          <button className="btn ghost" onClick={()=>nav("/imagenes")}>Tomar Imágenes</button>
          <button className="btn secondary" onClick={()=>nav("/imagenes")}>Subir Imágenes</button>
          <button className="btn" onClick={()=>nav("/imagenes")}>Adjuntar a Proyecto</button>
        </div>
      </section>
    </>
  );
}
