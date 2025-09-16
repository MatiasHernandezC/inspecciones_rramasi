import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { ProyectosAPI } from "../../services/proyectos";
import { ClientesAPI } from "../../services/clientes";

export default function ProyectosPage() {
  const nav = useNavigate();
  const [proyectos, setProyectos] = useState([]);
  const [clientes, setClientes] = useState([]);
  const [filtroCliente, setFiltroCliente] = useState("");

  useEffect(() => {
    ClientesAPI.listar({}).then(setClientes);
    ProyectosAPI.listar({}).then(setProyectos);
  }, []);

  const filtrarProyectos = proyectos.filter(p =>
    !filtroCliente || p.id_cliente === parseInt(filtroCliente)
  );

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold">Proyectos</h2>
        <button className="btn btn-primary" onClick={() => nav("/proyectos/nuevo")}>
          + Nuevo Proyecto
        </button>
      </div>

      <div className="mb-4 flex gap-2">
        <select
          value={filtroCliente}
          onChange={(e) => setFiltroCliente(e.target.value)}
          className="input w-64"
        >
          <option value="">Todos los Clientes</option>
          {clientes.map(c => (
            <option key={c.id_cliente} value={c.id_cliente}>{c.nombre}</option>
          ))}
        </select>
      </div>

      <div className="bg-white shadow rounded-lg overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nombre</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Cliente</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Número</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Estado</th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Acciones</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {filtrarProyectos.map(p => (
              <tr key={p.id_proyecto}>
                <td className="px-6 py-4 whitespace-nowrap">{p.nombre}</td>
                <td className="px-6 py-4 whitespace-nowrap">{clientes.find(c => c.id_cliente === p.id_cliente)?.nombre || "-"}</td>
                <td className="px-6 py-4 whitespace-nowrap">{p.numero || "-"}</td>
                <td className="px-6 py-4 whitespace-nowrap">{p.estado || "-"}</td>
                <td className="px-6 py-4 whitespace-nowrap text-right">
                  <button className="btn btn-secondary" onClick={() => nav(`/proyectos/${p.id_proyecto}/editar`)}>
                    Editar
                  </button>
                </td>
              </tr>
            ))}
            {filtrarProyectos.length === 0 && (
              <tr>
                <td colSpan={5} className="px-6 py-4 text-center text-gray-500">
                  No hay proyectos para mostrar
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
