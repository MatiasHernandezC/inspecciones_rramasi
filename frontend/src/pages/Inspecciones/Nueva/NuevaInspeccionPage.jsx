import React, { useMemo, useState } from "react";
import ToggleTri from "../../../components/ui/ToggleTri";

const encabezadoCampos = [
  { k: "cliente", label: "Cliente" },
  { k: "integrador", label: "Nombre Integrador" },
  { k: "proyecto", label: "Proyecto" },
  { k: "contacto", label: "Contacto" },
  { k: "numeroProyecto", label: "N° Proyecto" },
  { k: "lugar", label: "Lugar de Inspección" },
];

// Items demo (reemplazar por carga desde backend según tipo)
const itemsBase = [
  { id: "1.1", grupo: "PRESENTACIÓN", nombre:"Limpieza interna y externa" },
  { id: "1.2", grupo: "PRESENTACIÓN", nombre:"Cableado ordenado" },
  { id: "1.3", grupo: "PRESENTACIÓN", nombre:"Cortes y pintura" },
  { id: "2.1", grupo: "DOCUMENTACIÓN", nombre:"Carpeta técnica completa" },
  { id: "2.2", grupo: "DOCUMENTACIÓN", nombre:"Checklist Integrador presente" },
  { id: "3.1", grupo: "TABLERO", nombre:"Modelo según lo requerido" },
];

export default function NuevaInspeccionPage(){
  const [head, setHead] = useState({});
  const [res, setRes]   = useState({}); // { [id]: { v:"P"|"F"|"N", obs:"" } }

  const grupos = useMemo(()=>{
    const g = {};
    for(const it of itemsBase){ if(!g[it.grupo]) g[it.grupo] = []; g[it.grupo].push(it); }
    return Object.entries(g);
  }, []);

  const setValor = (id, patch) => setRes(s => ({ ...s, [id]: { ...(s[id]||{}), ...patch } }));

  return (
    <div>
      <h2 className="title" style={{fontSize:32}}>Nueva Inspección</h2>
      <p className="badge">Tablero tipo — configurable</p>

      {/* Encabezado técnico */}
      <div className="section">
        <h3 className="sectionTitle">Datos del Proyecto</h3>
        <div className="grid2">
          {encabezadoCampos.map(c => (
            <div key={c.k}>
              <label style={{fontWeight:700, fontSize:13}}>{c.label}</label>
              <input className="input" value={head[c.k]||""} onChange={e=>setHead(h=>({...h,[c.k]:e.target.value}))} />
            </div>
          ))}
        </div>
      </div>

      {/* Checklist */}
      {grupos.map(([nombreGrupo, items]) => (
        <div key={nombreGrupo} className="section">
          <h3 className="sectionTitle">{nombreGrupo}</h3>
          <table className="table">
            <thead>
              <tr className="trow">
                <th className="tcell" style={{width:100}}>Ítem</th>
                <th className="tcell">Descripción</th>
                <th className="tcell" style={{width:260}}>PASA / FALLA / N/A</th>
                <th className="tcell" style={{width:260}}>Observación</th>
              </tr>
            </thead>
            <tbody>
              {items.map(it => (
                <tr key={it.id} className="trow">
                  <td className="tcell">{it.id}</td>
                  <td className="tcell">{it.nombre}</td>
                  <td className="tcell">
                    <ToggleTri
                      name={`tri-${it.id}`}
                      value={res[it.id]?.v || ""}
                      onChange={(v)=>setValor(it.id, { v })}
                    />
                  </td>
                  <td className="tcell">
                    <input
                      className="input"
                      placeholder="Observación"
                      value={res[it.id]?.obs || ""}
                      onChange={(e)=>setValor(it.id, { obs: e.target.value })}
                    />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ))}

      <div className="row" style={{marginTop:16}}>
        <button className="btn secondary" onClick={()=>console.log({head, res})}>Guardar borrador</button>
        <button className="btn" onClick={()=>console.log("Enviar a backend para crear")}>Guardar y continuar</button>
      </div>
    </div>
  );
}
