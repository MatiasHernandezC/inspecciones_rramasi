import React, { useEffect, useState } from "react";
import { InspeccionesAPI } from "../../../services/inspecciones";
import { useNavigate } from "react-router-dom";
import { ArrowLeft, Home, Plus } from "lucide-react";

export default function InspeccionesPage() {
  const nav = useNavigate();
  const [rows, setRows] = useState([]);
  const [q, setQ] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const fetchInspecciones = async () => {
    setLoading(true);
    setError("");
    try {
      const data = await InspeccionesAPI.listar();
      setRows(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchInspecciones();
  }, []);

  const filtrarRows = rows.filter(
    (r) =>
      !q ||
      r.cliente.toLowerCase().includes(q.toLowerCase()) ||
      r.proyecto.toLowerCase().includes(q.toLowerCase())
  );

  return (
    <div className="container mx-auto px-4 sm:px-6 lg:px-8 mt-6">
      {/* ENCABEZADO */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-4 gap-3">
        <h2 className="text-2xl font-bold text-gray-800">Proyectos / Inspecciones</h2>
        <div className="flex flex-wrap gap-2">
          <button
            className="bg-gray-500 hover:bg-gray-600 text-white font-medium px-4 py-2 rounded-lg flex items-center gap-2"
            onClick={() => nav(-1)}
          >
            <ArrowLeft size={18} /> Volver
          </button>
          <button
            className="bg-blue-500 hover:bg-blue-600 text-white font-medium px-4 py-2 rounded-lg flex items-center gap-2"
            onClick={() => nav("/")}
          >
            <Home size={18} /> Inicio
          </button>
          <button
            className="bg-brand hover:bg-brand-light text-white font-medium px-4 py-2 rounded-lg flex items-center gap-2"
            onClick={() => nav("/inspecciones/nueva")}
          >
            <Plus size={18} /> Nueva
          </button>
        </div>
      </div>

      {/* FILTRO */}
      <div className="mb-4 flex flex-wrap gap-2 items-center">
        <input
          type="text"
          placeholder="Buscar por cliente, proyecto..."
          value={q}
          onChange={(e) => setQ(e.target.value)}
          className="w-full sm:w-64 border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-brand focus:border-brand transition"
        />
        <button
          className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium px-4 py-2 rounded-lg"
          onClick={fetchInspecciones}
        >
          Buscar
        </button>
      </div>

      {/* ESTADOS */}
      {loading && <p className="text-gray-600">Cargando inspecciones...</p>}
      {error && <p className="text-red-600">{error}</p>}
      {!loading && filtrarRows.length === 0 && (
        <p className="text-gray-600">No hay inspecciones registradas.</p>
      )}

      {/* TABLA */}
      {!loading && filtrarRows.length > 0 && (
        <div className="overflow-x-auto shadow-md rounded-lg border border-gray-200">
          <table className="min-w-full text-sm text-left text-gray-800 table-auto">
            <thead className="bg-gray-100 text-gray-700 uppercase text-xs font-semibold">
              <tr>
                <th className="px-4 py-3">Cliente</th>
                <th className="px-4 py-3">Proyecto</th>
                <th className="px-4 py-3">Fecha</th>
                <th className="px-4 py-3">Estado</th>
                <th className="px-4 py-3 text-center">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {filtrarRows.map((r, idx) => (
                <tr
                  key={r.id}
                  className={`border-t ${idx % 2 === 0 ? "bg-white" : "bg-gray-50"}`}
                >
                  <td className="px-4 py-2">{r.cliente}</td>
                  <td className="px-4 py-2">{r.proyecto}</td>
                  <td className="px-4 py-2">{new Date(r.fecha).toLocaleDateString()}</td>
                  <td className="px-4 py-2">
                    <span className="inline-block px-2 py-1 bg-gray-200 text-gray-800 rounded-md">
                      {r.estado}
                    </span>
                  </td>
                  <td className="px-4 py-2 text-center">
                    <div className="flex flex-wrap justify-center gap-2">
                      <button
                        className="bg-blue-500 hover:bg-blue-600 text-white px-3 py-1.5 rounded-md text-sm font-medium"
                        onClick={() => nav(`/inspecciones/${r.id}`)}
                      >
                        Abrir
                      </button>
                      <button
                        className="bg-gray-200 hover:bg-gray-300 text-gray-800 px-3 py-1.5 rounded-md text-sm font-medium"
                        onClick={() => InspeccionesAPI.generarInforme(r.id)}
                      >
                        Generar informe
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
