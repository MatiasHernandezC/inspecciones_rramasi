import React, { useEffect, useMemo, useState } from "react";
import { useParams } from "react-router-dom";
import ToggleTri from "../../../components/ui/ToggleTri";
import CellSelect from "../../../components/ui/CellSelect";
import { ClientesAPI } from "../../../services/clientes";
import { ProyectosAPI } from "../../../services/proyectos";
import { TablerosAPI } from "../../../services/tableros";
import { TiposTableroAPI } from "../../../services/tiposTablero";
import { ChecklistAPI } from "../../../services/checklist";
import { InspeccionesAPI } from "../../../services/inspecciones";
import { RespuestasAPI } from "../../../services/respuestas";
import { FotosAPI } from "../../../services/fotos";
import CropperMini from "../../../components/media/CropperMini";
import { IntegradoresAPI } from "../../../services/integradores";

export default function EditarInspeccionPage() {
  const { id } = useParams();
  const [clientes, setClientes] = useState([]);
  const [proyectos, setProyectos] = useState([]);
  const [tipos, setTipos] = useState([]);

  const [form, setForm] = useState({
    id_cliente: "",
    id_proyecto: "",
    id_tablero: "",
    id_tipo: "",
    codigo_tablero: "",
    observaciones: "",
    inspector: "",
    fecha_inspeccion: "",
    conclusion_calidad: "",
    num_solicitud_oc: "",
    num_producto: "",
    num_serie: "",
  });
  const [check, setCheck] = useState({ plantilla_id: null, version: null, items: [] });
  const [checkError, setCheckError] = useState("");
  const [res, setRes] = useState({});
  const [detalleTablero, setDetalleTablero] = useState(null);
  const [nombreIntegrador, setNombreIntegrador] = useState("");
  const [tipoTableroNombre, setTipoTableroNombre] = useState("");
  const [fotos, setFotos] = useState([]);

  useEffect(() => {
    (async () => {
      try {
        setClientes(await ClientesAPI.listar({ limit: 1000 }));
        setTipos(await TiposTableroAPI.listar({ limit: 1000 }));
        const insp = await InspeccionesAPI.obtener(id);
        // Proyecto y cliente para combos
        const prj = await ProyectosAPI.obtener(insp.id_proyecto);
        setProyectos(await ProyectosAPI.listarPorCliente(prj.id_cliente));
        // Tablero y tipo
        const tb = await TablerosAPI.obtener(insp.id_tablero);
        setDetalleTablero(tb);
        const tipo = tb.id_tipo ? await TiposTableroAPI.obtener(tb.id_tipo) : null;
        if (prj.id_integrador) {
          try {
            const integ = await IntegradoresAPI.obtener(prj.id_integrador);
            setNombreIntegrador(integ?.nombre || "");
          } catch (_) {}
        }
        setTipoTableroNombre(tipo?.nombre || "");
        setForm((f) => ({
          ...f,
          id_cliente: String(prj.id_cliente),
          id_proyecto: String(insp.id_proyecto),
          id_tablero: String(insp.id_tablero),
          id_tipo: tb.id_tipo ? String(tb.id_tipo) : "",
          codigo_tablero: tb.codigo_tablero || "",
          observaciones: insp.observaciones || "",
          inspector: insp.inspector || "",
          fecha_inspeccion: insp.fecha_inspeccion ? insp.fecha_inspeccion.substring(0,10) : "",
          conclusion_calidad: insp.conclusion_calidad || "",
          num_solicitud_oc: insp.num_solicitud_oc || "",
          num_producto: insp.num_producto || "",
          num_serie: insp.num_serie || "",
        }));
        // Checklist (por tablero)
        await loadChecklist(tb.id_tablero, tb.id_tipo);
        // Respuestas
        const rs = await RespuestasAPI.listarPorInspeccion(id);
        const map = {};
        for (const r of rs) {
          map[r.id_item] = { v: r.respuesta || "", obs: r.observacion || "" };
        }
        setRes(map);
        // Fotos de la inspección
        try {
          const lf = await FotosAPI.listarPorInspeccion(id);
          setFotos(lf.map(f => f.ruta_archivo));
        } catch (_) {}
      } catch (e) {
        console.error(e);
      }
    })();
  }, [id]);

  async function loadChecklist(tableroId, tipoId) {
    try {
      setCheckError("");
      const ck = tableroId
        ? await ChecklistAPI.resolverPorTablero(tableroId)
        : await ChecklistAPI.resolverPorTipo(tipoId);
      const items = (ck.items || []).map((it) => ({
        ...it,
        rules: typeof it.rules === "string" ? safeJson(it.rules) : it.rules,
      }));
      setCheck({ ...ck, items });
    } catch (e) {
      console.error(e);
      setCheck({ plantilla_id: null, version: null, items: [] });
      setCheckError(e?.message || "Error cargando checklist");
    }
  }

  const grupos = useMemo(() => {
    const g = {};
    for (const it of check.items) {
      const sec = it.seccion || "General";
      if (!g[sec]) g[sec] = [];
      g[sec].push(it);
    }
    return Object.entries(g);
  }, [check]);

  const setValor = (id_item, patch) =>
    setRes((s) => ({ ...s, [id_item]: { ...(s[id_item] || {}), ...patch } }));

  const guardar = async () => {
    try {
      const respuestas = Object.entries(res).map(([id_item, obj]) => ({
        id_item: Number(id_item),
        respuesta: obj.v ?? obj.valor ?? obj.respuesta ?? "",
        observacion: obj.obs || obj.observacion || "",
      }));
      if (respuestas.length) {
        await RespuestasAPI.bulkUpsert(id, respuestas);
      }
      await InspeccionesAPI.actualizar(id, {
        observaciones: form.observaciones,
        inspector: form.inspector || undefined,
        fecha_inspeccion: form.fecha_inspeccion || undefined,
        conclusion_calidad: form.conclusion_calidad || undefined,
        num_solicitud_oc: form.num_solicitud_oc || undefined,
        num_producto: form.num_producto || undefined,
        num_serie: form.num_serie || undefined,
        estado: "draft",
      });
      alert("Guardado");
    } catch (e) {
      console.error(e);
      alert(`Error al guardar: ${e.message}`);
    }
  };

  return (
    <div className="print-root">
      <h2 className="title" style={{ fontSize: 32 }}>Inspección #{id}</h2>

      <div className="section">
        <h3 className="sectionTitle">Información General</h3>
        <table className="table excel">
          <tbody>
            <tr>
              <td className="tcell" style={{width:180}}>Cliente</td>
              <td className="tcell">{(clientes.find(c=>String(c.id_cliente)===String(form.id_cliente))||{}).nombre || '-'}</td>
              <td className="tcell" style={{width:180}}>Nombre Integrador</td>
              <td className="tcell">{nombreIntegrador || '-'}</td>
            </tr>
            <tr>
              <td className="tcell">Proyecto</td>
              <td className="tcell">{(proyectos.find(p=>String(p.id_proyecto)===String(form.id_proyecto))||{}).nombre || '-'}</td>
              <td className="tcell">Contacto</td>
              <td className="tcell">{(clientes.find(c=>String(c.id_cliente)===String(form.id_cliente))||{}).contacto || '-'}</td>
            </tr>
            <tr>
              <td className="tcell">Tipo de Tablero</td>
              <td className="tcell">{tipoTableroNombre || '-'}</td>
              <td className="tcell">Codigo de Tablero</td>
              <td className="tcell">{form.codigo_tablero || '-'}</td>
            </tr>
            <tr>
              <td className="tcell">Nombre del Tablero</td>
              <td className="tcell">{detalleTablero?.codigo_tablero || form.codigo_tablero || '-'}</td>
              <td className="tcell">Lugar de Inspeccion</td>
              <td className="tcell">{detalleTablero?.ubicacion || '-'}</td>
            </tr>
            <tr>
              <td className="tcell">N° Sol. Prod. u O/C.</td>
              <td className="tcell"><input className="input" value={form.num_solicitud_oc} onChange={(e)=>setForm(f=>({...f,num_solicitud_oc:e.target.value}))} /></td>
              <td className="tcell">Inspector de Calidad</td>
              <td className="tcell"><input className="input" value={form.inspector} onChange={(e)=>setForm(f=>({...f,inspector:e.target.value}))} /></td>
            </tr>
            <tr>
              <td className="tcell">N° Producto</td>
              <td className="tcell"><input className="input" value={form.num_producto} onChange={(e)=>setForm(f=>({...f,num_producto:e.target.value}))} /></td>
              <td className="tcell">Fecha de Inspeccion</td>
              <td className="tcell"><input type="date" className="input" value={form.fecha_inspeccion} onChange={(e)=>setForm(f=>({...f,fecha_inspeccion:e.target.value}))} /></td>
            </tr>
            <tr>
              <td className="tcell">N° de Serie</td>
              <td className="tcell"><input className="input" value={form.num_serie} onChange={(e)=>setForm(f=>({...f,num_serie:e.target.value}))} /></td>
              <td className="tcell">Conclusion de Calidad</td>
              <td className="tcell"><input className="input" value={form.conclusion_calidad} onChange={(e)=>setForm(f=>({...f,conclusion_calidad:e.target.value}))} /></td>
            </tr>
            <tr>
              <td className="tcell">Observaciones</td>
              <td className="tcell" colSpan={3}>
                <textarea className="input" rows={3} value={form.observaciones} onChange={(e) => setForm((f) => ({ ...f, observaciones: e.target.value }))} />
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      {checkError && (
        <div className="section">
          <div className="text-red-600">{checkError}</div>
        </div>
      )}
      <div className="section">
      {grupos.map(([nombreGrupo, items]) => (
        
          <table className="table excel">
            <thead>
              <tr className="trow">
                <th className="tcell" colSpan={6} style={{ textAlign: 'left' }}>{sectionHeaderNumero(items)}.0 {nombreGrupo}</th>
              </tr>
              <tr className="trow">
                <th className="tcell" style={{ width: 70 }}>Item</th>
                <th className="tcell">Descripcion</th>
                <th className="tcell" style={{ width: 45, textAlign:'center' }}>Pasa</th>
                <th className="tcell" style={{ width: 45, textAlign:'center' }}>Falla</th>
                <th className="tcell" style={{ width: 45, textAlign:'center' }}>N/A</th>
                <th className="tcell" style={{ width: 220 }}>Observacion</th>
              </tr>
            </thead>
            <tbody>
              {items.map((it) => (
                <tr key={it.id} className="trow">
                  <td className="tcell">{extractNumero(it.label)}</td>
                  <td className="tcell">{extractDescripcion(it.label)}</td>
                  {renderValorCeldas(it, res[it.id]?.v || res[it.id]?.valor || "", (v)=>setValor(it.id, { v }))}
                  <td className="tcell">
                    <textarea
                      className="w-full resize-none focus:outline-none bg-transparent overflow-hidden"
                      placeholder="Observacion"
                      value={res[it.id]?.obs || ""}
                      onChange={(e) => {
                        setValor(it.id, { obs: e.target.value });
                        // Ajuste automático del alto
                        e.target.style.height = "auto";
                        e.target.style.height = `${e.target.scrollHeight}px`;
                      }}
                      rows={1} // empieza como una línea
                    />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        
      ))}
      </div>
      <div className="section">
        <h3 className="sectionTitle no-print">Registro fotografico (basico)</h3>
        <div className="no-print" style={{maxWidth:360}}>
          <CropperMini onCropped={async (dataUrl)=>{
          try{
            await FotosAPI.crear({ id_proyecto: Number(form.id_proyecto), id_tablero: Number(form.id_tablero), id_inspeccion: Number(id), ruta_archivo: dataUrl, metadatos: JSON.stringify({ source: 'cropperMini', ts: Date.now() }) });
            alert('Foto guardada');
            setFotos(prev => [...prev, dataUrl]);
          }catch(e){ console.error(e); alert(`Error guardando foto: ${e.message}`); }
        }} />
        </div>
        {fotos.length > 0 && (
          <div className="photos-grid" style={{marginTop:12}}>
            {fotos.map((src, i)=> (
              <img key={i} className="photo-item" src={src} alt={`Foto ${i+1}`} />
            ))}
          </div>
        )}
      </div>

      <div className="row no-print" style={{marginTop:16, justifyContent:'flex-end'}}>
        <button className="btn secondary" onClick={()=>window.print()}>Generar Informe</button>
        <button className="btn" onClick={guardar}>Guardar</button>
      </div>
    </div>
  );
}

function safeJson(s){ try{ return JSON.parse(s); }catch(_){ return null; } }
function extractNumero(label){ if(!label) return ""; const m=String(label).trim().match(/^([0-9]+(?:\.[0-9]+)*)\b/); return m?m[1]:""; }
function extractDescripcion(label){ if(!label) return ""; return String(label).trim().replace(/^([0-9]+(?:\.[0-9]+)*)\s*/, ""); }
function renderInput(item, value, onChange){
  const t = item.type;
  const rules = item.rules || {};
  if (t === "boolean") {
    return (
      <CellSelect
        value={value}
        onChange={onChange}
        options={["PASA","FALLA","N/A"]}
        className="w-full"
      />
    );
  }
  if (t === "number") {
    return (
      <input type="number" className="input" value={value} onChange={(e)=>onChange(e.target.value)} min={rules.min} max={rules.max} />
    );
  }
  if (t === "select") {
    const opts = rules.options || [];
    return (<CellSelect value={value} onChange={onChange} options={opts} className="w-full" />);
  }
  if (t === "text") {
    return (<input className="input" value={value} onChange={(e)=>onChange(e.target.value)} />);
  }
  return (<input className="input" value={value} onChange={(e)=>onChange(e.target.value)} />);
}
function sectionHeaderNumero(items) {
  if (!items || !items.length) return '';
  const first = items[0];
  const num = extractNumero(first.label);
  return (num && String(num).split('.')[0]) || '';
}
function renderValorCeldas(item, value, onChange){
  const t = item.type;
  if (t === 'boolean'){
    const sel = String(value || '').toUpperCase();
    const mk = (key) => (
      <td className="tcell" style={{textAlign:'center', cursor:'pointer', backgroundColor: sel===key ? '#eee' : 'transparent'}} onClick={()=>onChange(key)}>
        <span>{sel === key ? ' ✓' : ' '}</span>
      </td>
    );
    return (<>
      {mk('PASA')}
      {mk('FALLA')}
      {mk('N/A')}
    </>);
  }
  return (
    <td className="tcell" colSpan={3}>
      {renderInput(item, value, onChange)}
    </td>
  );
}

