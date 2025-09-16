import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { FotosAPI } from "../../services/fotos";
import { InspeccionesAPI } from "../../services/inspecciones";
import CropperMini from "../../components/media/CropperMini";
import { useFotos } from "../../hooks/useFotos";

export default function GestorImagenesPage() {
  const nav = useNavigate();
  const [inspecciones, setInspecciones] = useState([]);
  const [idInspeccion, setIdInspeccion] = useState(null);
  const fotos = useFotos(idInspeccion);

  useEffect(() => {
    (async () => {
      const list = await InspeccionesAPI.listar({ limit: 100 });
      setInspecciones(list);
    })();
  }, []);

  const dataURLtoFile = (dataurl, filename) => {
    const arr = dataurl.split(',');
    const mime = arr[0].match(/:(.*?);/)[1];
    const bstr = atob(arr[1]);
    let n = bstr.length;
    const u8arr = new Uint8Array(n);
    while (n--) u8arr[n] = bstr.charCodeAt(n);
    return new File([u8arr], filename, { type: mime });
  };

  const subirFoto = async (dataUrl) => {
    if (!idInspeccion) return alert("Selecciona una inspección");

    const inspeccion = inspecciones.find(i => i.id === idInspeccion);
    if (!inspeccion) return alert("Inspección no encontrada");
    // Revisa los nombres reales de las propiedades
    const idProyecto = inspeccion.id_proyecto ?? inspeccion.proyecto_id ?? null;
    const idTablero = inspeccion.id_tablero ?? inspeccion.tablero_id ?? null;

    if (!idProyecto && !idTablero) {
      console.warn("La inspección no tiene proyecto ni tablero, la foto no se puede subir");
      return alert("Inspección sin proyecto ni tablero asignado");
    }
    
    const file = dataURLtoFile(dataUrl, "foto.jpg");

    try {
      console.log("Subiendo foto con datos:", {
        file,
        id_inspeccion: idInspeccion,
        id_proyecto: inspeccion.id_proyecto,
        id_tablero: inspeccion.id_tablero,
        fecha_captura: new Date().toISOString()
      });

      await FotosAPI.crear({
        file,
        id_inspeccion: idInspeccion,
        id_proyecto: inspeccion.id_proyecto || 0, // asegurar que no sea undefined
        id_tablero: inspeccion.id_tablero || 0,
        fecha_captura: new Date().toISOString()
      });

      alert("Foto subida correctamente!");
    } catch (e) {
      console.error("Error subiendo foto:", e);
      alert(`Error subiendo foto: ${e.message}`);
    }
  };

  return (
    <div>
      <h2>Gestor de Imágenes</h2>

      <div>
        <label>Seleccionar Inspección:</label>
        <select value={idInspeccion || ""} onChange={e => setIdInspeccion(Number(e.target.value))}>
          <option value="">-- Seleccionar --</option>
          {inspecciones.map(i => (
            <option key={i.id} value={i.id}>
              {i.proyecto} - {i.cliente} ({i.fecha})
            </option>
          ))}
        </select>
      </div>

      <div style={{marginTop: 16}}>
        <h3>Subir / Recortar Foto</h3>
        <CropperMini onCropped={subirFoto} />
      </div>

      <div style={{marginTop: 16}}>
        <h3>Fotos Subidas</h3>
        <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
          {fotos && fotos.length > 0 ? fotos.map((src,i)=>(
            <img key={i} src={src} alt={`Foto ${i+1}`} style={{ width: 150, height: 150, objectFit: "cover", border: "1px solid #ccc" }} />
          )) : <p>No hay fotos subidas</p>}
        </div>
      </div>
    </div>
  );
}
