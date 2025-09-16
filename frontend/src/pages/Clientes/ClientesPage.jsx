// src/pages/Clientes/ClientesPage.jsx
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { ClientesAPI } from "../../services/clientes";

export default function ClientesPage() {
  const nav = useNavigate();
  const [clientes, setClientes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Cargar clientes al montar el componente
  useEffect(() => {
    fetchClientes();
  }, []);

  const fetchClientes = async () => {
    setLoading(true);
    setError("");
    try {
      const data = await ClientesAPI.listar();
      setClientes(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleEliminar = async (id_cliente) => {
    if (!window.confirm("¿Seguro que quieres eliminar este cliente?")) return;

    try {
      await ClientesAPI.eliminar(id_cliente);
      setClientes((prev) => prev.filter((c) => c.id_cliente !== id_cliente));
    } catch (err) {
      alert("Error al eliminar: " + err.message);
    }
  };

  return (
    <div className="container mx-auto mt-6">
      <h2 className="text-2xl font-bold mb-4">Clientes</h2>

      <button
        className="btn mb-4"
        onClick={() => nav("/clientes/nuevo")}
      >
        Nuevo Cliente
      </button>

      {loading && <p>Cargando clientes...</p>}
      {error && <p className="text-red-600">{error}</p>}

      {!loading && clientes.length === 0 && <p>No hay clientes registrados.</p>}

      {!loading && clientes.length > 0 && (
        <table className="table-auto w-full border border-gray-300">
          <thead>
            <tr className="bg-gray-200">
              <th className="px-4 py-2">ID</th>
              <th className="px-4 py-2">Nombre</th>
              <th className="px-4 py-2">Alias</th>
              <th className="px-4 py-2">Contacto</th>
              <th className="px-4 py-2">Teléfono</th>
              <th className="px-4 py-2">Email</th>
              <th className="px-4 py-2">Acciones</th>
            </tr>
          </thead>
          <tbody>
            {clientes.map((c) => (
              <tr key={c.id_cliente} className="border-t">
                <td className="px-4 py-2">{c.id_cliente}</td>
                <td className="px-4 py-2">{c.nombre}</td>
                <td className="px-4 py-2">{c.alias || "-"}</td>
                <td className="px-4 py-2">{c.contacto || "-"}</td>
                <td className="px-4 py-2">{c.telefono || "-"}</td>
                <td className="px-4 py-2">{c.email || "-"}</td>
                <td className="px-4 py-2 space-x-2">
                  <button
                    className="btn secondary btn-sm"
                    onClick={() => nav(`/clientes/editar/${c.id_cliente}`)}
                  >
                    Editar
                  </button>
                  <button
                    className="btn btn-sm ghost"
                    onClick={() => handleEliminar(c.id_cliente)}
                  >
                    Eliminar
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
