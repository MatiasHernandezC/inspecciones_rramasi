import React, { useEffect, useMemo, useState } from "react";
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
import { Divider } from "@mui/material";
import { BorderColor } from "@mui/icons-material";

export default function NuevaInspeccionPage() {
  const [clientes, setClientes] = useState([]);
  const [proyectos, setProyectos] = useState([]);
  const [tableros, setTableros] = useState([]);
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
  const [inspeccionId, setInspeccionId] = useState(null);
  const [check, setCheck] = useState({ plantilla_id: null, version: null, items: [] });
  const [checkError, setCheckError] = useState("");
  const [res, setRes] = useState({});
  const [detalleProyecto, setDetalleProyecto] = useState(null);
  const [detalleTablero, setDetalleTablero] = useState(null);
  const [nombreIntegrador, setNombreIntegrador] = useState("");
  const [tipoTableroNombre, setTipoTableroNombre] = useState("");
  const [fotos, setFotos] = useState([]);
  // Si ya existe inspección, cargar fotos para imprimir
  useEffect(()=>{ (async()=>{
    if(!inspeccionId) return;
    try{
      const list = await FotosAPI.listarPorInspeccion(inspeccionId);
      setFotos(list.map(f=>f.ruta_archivo));
    }catch(e){ console.error(e); }
  })(); }, [inspeccionId]);

  
  useEffect(() => {
    (async () => {
      try {
        const cls = await ClientesAPI.listar({ limit: 1000 });
        setClientes(cls);
        const tps = await TiposTableroAPI.listar({ limit: 1000 });
        setTipos(tps);
      } catch (e) {
        console.error(e);
      }
    })();
  }, []);

  useEffect(() => {
    (async () => {
      if (!form.id_cliente) {
        setProyectos([]);
        return;
      }
      try {
        const list = await ProyectosAPI.listarPorCliente(form.id_cliente);
        setProyectos(list);
      } catch (e) {
        console.error(e);
        setProyectos([]);
      }
    })();
  }, [form.id_cliente]);

  useEffect(() => {
    (async () => {
      if (!form.id_proyecto) {
        setTableros([]);
        setDetalleProyecto(null);
        setNombreIntegrador("");
        return;
      }
      try {
        setTableros(await TablerosAPI.listarPorProyecto(form.id_proyecto));
        const prj = await ProyectosAPI.obtener(form.id_proyecto);
        setDetalleProyecto(prj);
        if (prj.id_integrador) {
          try {
            const integ = await IntegradoresAPI.obtener(prj.id_integrador);
            setNombreIntegrador(integ?.nombre || "");
          } catch (_) {
            setNombreIntegrador("");
          }
        } else {
          setNombreIntegrador("");
        }
      } catch (e) {
        console.error(e);
        setTableros([]);
      }
    })();
  }, [form.id_proyecto]);

  useEffect(() => {
    (async () => {
      if (!form.id_tablero) {
        setCheck({ plantilla_id: null, version: null, items: [] });
        setCheckError("");
        setDetalleTablero(null);
        setTipoTableroNombre("");
        return;
      }
      try {
        setCheckError("");
        const ck = await ChecklistAPI.resolverPorTablero(form.id_tablero);
        const items = (ck.items || []).map((it) => ({
          ...it,
          rules: typeof it.rules === "string" ? safeJson(it.rules) : it.rules,
        }));
        setCheck({ ...ck, items });
        try {
          const tb = await TablerosAPI.obtener(form.id_tablero);
          setDetalleTablero(tb);
          if (tb.id_tipo) {
            try {
              const tipo = await TiposTableroAPI.obtener(tb.id_tipo);
              setTipoTableroNombre(tipo?.nombre || "");
            } catch (_) {}
          }
        } catch (_) {}
      } catch (e) {
        console.error(e);
        setCheck({ plantilla_id: null, version: null, items: [] });
        setCheckError(e?.message || "Error cargando checklist");
      }
    })();
  }, [form.id_tablero]);

  // Precarga por tipo seleccionado (si no hay tablero aún)
  useEffect(() => {
    (async () => {
      if (!form.id_tipo) return;
      try {
        const ck = await ChecklistAPI.resolverPorTipo(form.id_tipo);
        const items = (ck.items || []).map((it) => ({
          ...it,
          rules: typeof it.rules === "string" ? safeJson(it.rules) : it.rules,
        }));
        setCheck({ ...ck, items });
        const t = tipos.find((x) => String(x.id_tipo) === String(form.id_tipo));
        setTipoTableroNombre(t?.nombre || "");
      } catch (e) {
        console.error(e);
        setCheck({ plantilla_id: null, version: null, items: [] });
        setCheckError(e?.message || "Error cargando checklist por tipo");
      }
    })();
  }, [form.id_tipo]);

  const ensureTableroId = async () => {
    if (form.id_tablero) return Number(form.id_tablero);
    if (!form.id_proyecto || !form.codigo_tablero) return null;
    try {
      const list = await TablerosAPI.listarPorProyecto(form.id_proyecto);
      const found = list.find(
        (t) => String(t.codigo_tablero) === String(form.codigo_tablero)
      );
      if (found) return found.id_tablero;
    } catch (_) {}
    if (form.id_tipo) {
      try {
        const created = await TablerosAPI.crear({
          id_proyecto: Number(form.id_proyecto),
          id_tipo: Number(form.id_tipo),
          codigo_tablero: String(form.codigo_tablero),
          descripcion: "",
          ubicacion: "",
        });
        return created.id_tablero;
      } catch (e) {
        console.error(e);
      }
    }
    return null;
  };

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

  const crearBorrador = async () => {
    if (!form.id_proyecto || !form.id_tablero) {
      const tid = await ensureTableroId();
      if (!tid) {
        alert("Selecciona proyecto, tipo y código de tablero");
        return;
      }
      setForm((f) => ({ ...f, id_tablero: String(tid) }));
    }
    const payload = {
      id_proyecto: Number(form.id_proyecto),
      id_tablero: Number(form.id_tablero || (await ensureTableroId())),
      inspector: form.inspector || undefined,
      fecha_inspeccion: form.fecha_inspeccion || undefined,
      conclusion_calidad: form.conclusion_calidad || undefined,
      num_solicitud_oc: form.num_solicitud_oc || undefined,
      num_producto: form.num_producto || undefined,
      num_serie: form.num_serie || undefined,
      estado: "Sin Pagar",
    };
    const created = await InspeccionesAPI.crear(payload);
    setInspeccionId(created.id_inspeccion);
    return created.id_inspeccion;
  };

  const guardarContinuar = async () => {
    try {
      let id = inspeccionId;
      if (!id) {
        id = await crearBorrador();
      }
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
  const onCropped = async (dataUrl) => {
    try {
      let id = inspeccionId || await crearBorrador();
      await FotosAPI.crear({
        id_proyecto: Number(form.id_proyecto),
        id_tablero: Number(form.id_tablero),
        id_inspeccion: Number(id),
        ruta_archivo: dataUrl,
        metadatos: JSON.stringify({ source: "cropperMini", ts: Date.now() }),
      });
      // 1) feedback
      alert("Foto guardada");
      // 2) que se vea inmediatamente en UI e impresión
      setFotos(prev => [...prev, dataUrl]);
    } catch (e) {
      console.error(e);
      alert(`Error guardando foto: ${e.message}`);
    }
  };
  return (
      <div className="print-root">
        <div className="flex items-center justify-between mb-6 border-b border-slate-300 pb-2">
        <img src="/logo.png" alt="Logo Empresa" className="h-14" />
        <div className="text-center flex-1">
          <h1 className="text-2xl font-bold text-slate-900">Informe de Inspección</h1>
          <p className="text-sm text-slate-600">{detalleProyecto?.nombre || "-"}</p>
        </div>
        <span className="text-sm text-slate-500">
          Fecha: {form.fecha_inspeccion || "-"}
        </span>
      </div>
      <h2 className="title" style={{ fontSize: 32 }}>Nueva Inspección</h2>
      <div className="section">
      <h3 className="sectionTitle">Información General</h3>
        <table className="table excel">
          <tbody>
            <tr>
              <td className="tcell" style={{width:180}}>Cliente</td>
              <td className="tcell">
                <select
                  className="w-full border-0 focus:outline-none bg-transparent"
                  value={form.id_cliente}
                  onChange={(e) => setForm((f) => ({ ...f, id_cliente: e.target.value, id_proyecto: "", id_tablero: "" }))}
                >
                  <option value="">-- Seleccionar --</option>
                  {clientes.map((c) => (
                    <option key={c.id_cliente} value={c.id_cliente}>{c.nombre}</option>
                  ))}
                </select>
              </td>
              <td className="tcell" style={{width:180}}>Nombre Integrador</td>
              <td className="tcell">{nombreIntegrador || '-'}</td>
            </tr>
            <tr>
              <td className="tcell">Proyecto</td>
              <td className="tcell">
                <select  className="w-full border-0 focus:outline-none bg-transparent" value={form.id_proyecto} onChange={(e) => setForm((f) => ({ ...f, id_proyecto: e.target.value, id_tablero: "" }))}>
                  <option value="">-- Seleccionar --</option>
                  {proyectos.map((p) => (<option key={p.id_proyecto} value={p.id_proyecto}>{p.nombre}</option>))}
                </select>
              </td>
              <td className="tcell">Contacto</td>
              <td className="tcell">{(clientes.find(c=>String(c.id_cliente)===String(form.id_cliente))||{}).contacto || '-'}</td>
            </tr>
            <tr>
              <td className="tcell">Tipo de Tablero</td>
              <td className="tcell">
                <select  className="w-full border-0 focus:outline-none bg-transparent" value={form.id_tipo} onChange={(e)=>setForm(f=>({...f,id_tipo:e.target.value}))}>
                  <option value="">-- Seleccionar --</option>
                  {tipos.map((t)=>(<option key={t.id_tipo} value={t.id_tipo}>{t.nombre}</option>))}
                </select>
              </td>
              <td className="tcell">Codigo de Tablero</td>
              <td className="tcell"><input className="w-full border-0 focus:outline-none bg-transparent" value={form.codigo_tablero} onChange={(e)=>setForm(f=>({...f,codigo_tablero:e.target.value}))} placeholder="Ej: TAB-001" /></td>
            </tr>
            <tr>
              <td className="tcell">Nombre del Tablero</td>
              <td className="tcell">{detalleTablero?.codigo_tablero || form.codigo_tablero || '-'}</td>
              <td className="tcell">Lugar de Inspeccion</td>
              <td className="tcell">{detalleTablero?.ubicacion || '-'}</td>
            </tr>
            <tr>
              <td className="tcell">N° Sol. Prod. u O/C.</td>
              <td className="tcell"><input  className="w-full border-0 focus:outline-none bg-transparent" value={form.num_solicitud_oc} onChange={(e)=>setForm(f=>({...f,num_solicitud_oc:e.target.value}))} /></td>
              <td className="tcell">Inspector de Calidad</td>
              <td className="tcell"><input  className="w-full border-0 focus:outline-none bg-transparent" value={form.inspector} onChange={(e)=>setForm(f=>({...f,inspector:e.target.value}))} /></td>
            </tr>
            <tr>
              <td className="tcell">N° Producto</td>
              <td className="tcell"><input  className="w-full border-0 focus:outline-none bg-transparent" value={form.num_producto} onChange={(e)=>setForm(f=>({...f,num_producto:e.target.value}))} /></td>
              <td className="tcell">Fecha de Inspeccion</td>
              <td className="tcell"><input type="date"  className="w-full border-0 focus:outline-none bg-transparent" value={form.fecha_inspeccion} onChange={(e)=>setForm(f=>({...f,fecha_inspeccion:e.target.value}))} /></td>
            </tr>
            <tr>
              <td className="tcell">N° de Serie</td>
              <td className="tcell"><input  className="w-full border-0 focus:outline-none bg-transparent" value={form.num_serie} onChange={(e)=>setForm(f=>({...f,num_serie:e.target.value}))} /></td>
              <td className="tcell">Conclusion de Calidad</td>
              <td className="tcell"><input  className="w-full border-0 focus:outline-none bg-transparent" value={form.conclusion_calidad} onChange={(e)=>setForm(f=>({...f,conclusion_calidad:e.target.value}))} /></td>
            </tr>
            <tr>
              <td className="tcell">Observaciones</td>
              <td className="tcell" colSpan={3}>
                <textarea  
                  className="w-full border-0 focus:outline-none bg-transparent" 
                  rows={3} value={form.observaciones} 
                  onChange={(e) => setForm((f) => ({ ...f, observaciones: e.target.value }))} />
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      {checkError && form.id_tablero && (
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
                <th className="tcell w-[30px]">Item</th>
                <th className="tcell">Descripcion</th>
                <th className="tcell w-[45px] text-center">Pasa</th>
                <th className="tcell w-[45px] text-center">Falla</th>
                <th className="tcell w-[45px] text-center">N/A</th>
                <th className="tcell w-[260px]">Observacion</th>
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

      {/* Vista para imprimir: sí se muestra */}
      {fotos.length > 0 && (
        <div className="section">
  <h3 className="sectionTitle">Registro fotográfico</h3>
  <div className="photos-grid mt-2">
    {fotos.map((src, i) => (
      <figure key={i} className="text-center">
        <img src={src} alt={`Foto ${i+1}`} className="photo-item" />
        <figcaption className="text-xs text-slate-600 mt-1">Foto {i+1}</figcaption>
      </figure>
    ))}
  </div>
</div>

      )}

      {/* Herramienta de captura: no se imprime por .no-print */}
      <div className="section">
        <h3 className="sectionTitle no-print">Registro fotográfico (básico)</h3>
        <div className="row">
          <div className="no-print" style={{maxWidth:360}}>
            <CropperMini onCropped={onCropped} />
          </div>
        </div>
        {fotos.length > 0 && (
          <div className="photos-grid" style={{marginTop:12}}>
            {fotos.map((src, idx) => (
              <img key={idx} className="photo-item" src={src} alt={`Foto ${idx+1}`} />
            ))}
          </div>
        )}
      </div>

      <div className="row no-print" style={{ marginTop: 16, justifyContent:'flex-end' }}>
        <button className="btn secondary" onClick={()=>window.print()}>Generar Informe</button>
        <button className="btn secondary" onClick={crearBorrador}>Guardar borrador</button>
        <button className="btn" onClick={guardarContinuar}>Guardar y continuar</button>
      </div>
    </div>
  );
}

function safeJson(s) {
  try {
    return JSON.parse(s);
  } catch (_) {
    return null;
  }
}

function extractNumero(label) {
  if (!label) return "";
  const m = String(label).trim().match(/^([0-9]+(?:\.[0-9]+)*)\b/);
  return m ? m[1] : "";
}

function extractDescripcion(label) {
  if (!label) return "";
  return String(label).trim().replace(/^([0-9]+(?:\.[0-9]+)*)\s*/, "");
}

function renderInput(item, value, onChange) {
  const t = item.type;
  const rules = item.rules || {};
  if (t === "boolean") {
    return (
      <CellSelect
        value={value}
        onChange={onChange}
        options={["PASA", "FALLA", "N/A"]}
        className="w-full"
      />
    );
  }
  if (t === "number") {
    return (
      <input
        type="number"
        className="input"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        min={rules.min}
        max={rules.max}
      />
    );
  }
  if (t === "select") {
    const opts = rules.options || [];
    return (
      <CellSelect value={value} onChange={onChange} options={opts} className="w-full" />
    );
  }
  if (t === "text") {
    return <input  className="w-full border-0 focus:outline-none bg-transparent" value={value} onChange={(e) => onChange(e.target.value)} />;
  }
  return <input  className="w-full border-0 focus:outline-none bg-transparent" value={value} onChange={(e) => onChange(e.target.value)} />;
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


