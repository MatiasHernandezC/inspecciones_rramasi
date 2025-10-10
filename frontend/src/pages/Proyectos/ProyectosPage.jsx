import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { ProyectosAPI } from "../../services/proyectos";
import { ClientesAPI } from "../../services/clientes";
import { ArrowLeft, Home, Edit, Plus } from "lucide-react";

export default function ProyectosPage() {
  const nav = useNavigate();
  const [proyectos, setProyectos] = useState([]);
  const [clientes, setClientes] = useState([]);
  const [filtroCliente, setFiltroCliente] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const clientesData = await ClientesAPI.listar();
        setClientes(clientesData);
        const proyectosData = await ProyectosAPI.listar();
        setProyectos(proyectosData);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const filtrarProyectos = proyectos.filter(
    (p) => !filtroCliente || p.id_cliente === parseInt(filtroCliente)
  );

  return (
    <div className="container mx-auto px-4 sm:px-6 lg:px-8 mt-6">
      {/* ENCABEZADO */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-4 gap-3">
        <h2 className="text-2xl font-bold text-gray-800">Proyectos</h2>
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
            onClick={() => nav("/proyectos/nuevo")}
          >
            <Plus size={18} /> Nuevo Proyecto
          </button>
        </div>
      </div>

      {/* ESTADOS */}
      {loading && <p className="text-gray-600">Cargando proyectos...</p>}
      {error && <p className="text-red-600">{error}</p>}
      {!loading && filtrarProyectos.length === 0 && (
        <p className="text-gray-600">No hay proyectos registrados.</p>
      )}

      {/* FILTRO CLIENTE SOLO EN PANTALLA GRANDE */}
      {!loading && clientes.length > 0 && (
        <div className="mb-4 flex flex-wrap gap-2 hidden sm:flex">
          <select
            value={filtroCliente}
            onChange={(e) => setFiltroCliente(e.target.value)}
            className="border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-brand focus:border-brand"
          >
            <option value="">Todos los Clientes</option>
            {clientes.map((c) => (
              <option key={c.id_cliente} value={c.id_cliente}>
                {c.nombre}
              </option>
            ))}
          </select>
        </div>
      )}

      {/* TABLA */}
      {!loading && filtrarProyectos.length > 0 && (
        <div className="overflow-x-auto shadow-md rounded-lg border border-gray-200">
          <table className="table-auto min-w-full text-sm text-left text-gray-800">
            <thead className="bg-gray-100 text-gray-700 uppercase text-xs font-semibold">
              <tr>
                <th className="px-4 py-3 max-w-[70px]">Nombre</th>
                <th className="px-4 py-3 hidden sm:table-cell">Cliente</th>
                <th className="px-4 py-3 max-w-[70px]">Número</th>
                <th className="px-4 py-3 max-w-[70px]">Estado</th>
                <th className="px-4 py-3 text-center">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {filtrarProyectos.map((p, idx) => (
                <tr
                  key={p.id_proyecto}
                  className={`border-t ${idx % 2 === 0 ? "bg-white" : "bg-gray-50"}`}
                >
                  <td className="px-4 py-2 truncate max-w-[70px]" title={p.nombre}>
                    {p.nombre}
                  </td>
                  <td className="px-4 py-2 hidden sm:table-cell">
                    {clientes.find((c) => c.id_cliente === p.id_cliente)?.nombre || "-"}
                  </td>
                  <td className="px-4 py-2 max-w-[100px]">{p.numero || "-"}</td>
                  <td className="px-4 py-2 truncate max-w-[70px]" title={p.estado}>
                    {p.estado || "-"}
                  </td>
                  <td className="px-4 py-2 text-center">
                    <div className="flex justify-center gap-3">
                      <button
                        className="bg-blue-500 hover:bg-blue-600 text-white px-3 py-1.5 rounded-md text-sm font-medium flex items-center gap-1 transition"
                        onClick={() => nav(`/proyectos/${p.id_proyecto}/editar`)}
                      >
                        <Edit size={16} /> Editar
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
