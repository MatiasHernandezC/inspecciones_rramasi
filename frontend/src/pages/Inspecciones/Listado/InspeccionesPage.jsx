import React, { useEffect, useState } from "react";
import { InspeccionesAPI } from "../../../services/inspecciones";
import { useNavigate } from "react-router-dom";

export default function InspeccionesPage(){
  const [q, setQ] = useState("");
  const [rows, setRows] = useState([]);
  const nav = useNavigate();

  useEffect(()=>{ (async()=>{
    try{ setRows(await InspeccionesAPI.listar("")); }catch(e){ console.error(e); }
  })(); },[]);

  return (
    <div>
      <h2 className="title" style={{fontSize:32}}>Proyectos / Inspecciones</h2>
      <div className="section">
        <div className="row">
          <input className="input" placeholder="Buscar por cliente, proyecto..." value={q} onChange={e=>setQ(e.target.value)} />
          <button className="btn secondary" onClick={async()=>setRows(await InspeccionesAPI.listar(q))}>Buscar</button>
          <div className="spacer"/>
          <button className="btn" onClick={()=>nav("/inspecciones/nueva")}>Nueva</button>
        </div>
      </div>

      <div className="section">
        <table className="table">
          <thead>
            <tr className="trow">
              <th className="tcell">Cliente</th>
              <th className="tcell">Proyecto</th>
              <th className="tcell">Fecha</th>
              <th className="tcell">Estado</th>
              <th className="tcell" style={{width:160}}></th>
            </tr>
          </thead>
          <tbody>
            {rows.map(r => (
              <tr key={r.id} className="trow">
                <td className="tcell">{r.cliente}</td>
                <td className="tcell">{r.proyecto}</td>
                <td className="tcell">{new Date(r.fecha).toLocaleDateString()}</td>
                <td className="tcell"><span className="badge">{r.estado}</span></td>
                <td className="tcell">
                  <div className="row">
                    <button className="btn secondary" onClick={()=>nav(`/inspecciones/${r.id}`)}>Abrir</button>
                    <button className="btn" onClick={()=>InspeccionesAPI.generarInforme(r.id)}>Generar informe</button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
