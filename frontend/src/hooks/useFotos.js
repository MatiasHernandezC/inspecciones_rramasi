import { useEffect, useState } from "react";
import { FotosAPI } from "../services/fotos";

export function useFotos(idInspeccion) {
  const [fotos, setFotos] = useState([]);

  useEffect(() => {
    if (!idInspeccion) return;

    (async () => {
      try {
        const lista = await FotosAPI.listarPorInspeccion(idInspeccion);
        setFotos(lista.map(f => f.ruta_archivo));
      } catch (e) {
        console.error("Error cargando fotos:", e);
      }
    })();
  }, [idInspeccion]);

  return fotos;
}
