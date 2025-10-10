import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { ClientesAPI } from "../../services/clientes";
import { Mail, MessageCircle, ArrowLeft, Home, Edit, Trash2 } from "lucide-react";

export default function ClientesPage() {
  const nav = useNavigate();
  const [clientes, setClientes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

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

  const handleWhatsApp = (telefono) => {
    if (!telefono) return alert("Este cliente no tiene teléfono registrado.");
    const link = `https://wa.me/${telefono.replace(/\D/g, "")}`;
    window.open(link, "_blank");
  };

  const handleEmail = (email) => {
    if (!email) return alert("Este cliente no tiene correo registrado.");
    window.location.href = `mailto:${email}`;
  };

  return (
    <div className="container mx-auto px-4 sm:px-6 lg:px-8 mt-6">
      {/* ENCABEZADO */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-4 gap-3">
        <h2 className="text-2xl font-bold text-gray-800">Clientes</h2>
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
            onClick={() => nav("/clientes/nuevo")}
          >
            Nuevo Cliente
          </button>
        </div>
      </div>

      {/* ESTADOS */}
      {loading && <p className="text-gray-600">Cargando clientes...</p>}
      {error && <p className="text-red-600">{error}</p>}
      {!loading && clientes.length === 0 && (
        <p className="text-gray-600">No hay clientes registrados.</p>
      )}

      {/* TABLA */}
      {!loading && clientes.length > 0 && (
        <div className="overflow-x-auto shadow-md rounded-lg border border-gray-200">
          <table className="table-auto min-w-full text-sm text-left text-gray-800">
            <thead className="bg-gray-100 text-gray-700 uppercase text-xs font-semibold">
              <tr>
                <th className="px-4 py-3">Nombre</th>
                <th className="px-4 py-3 hidden md:table-cell">Alias</th>
                <th className="px-4 py-3 hidden md:table-cell">Contacto</th>
                <th className="px-4 py-3">Teléfono</th>
                <th className="px-4 py-3">Email</th>
                <th className="px-4 py-3 text-center">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {clientes.map((c, idx) => (
                <tr
                  key={c.id_cliente}
                  className={`border-t ${idx % 2 === 0 ? "bg-white" : "bg-gray-50"}`}
                >
                  <td className="px-4 py-2">{c.nombre}</td>
                  <td className="px-4 py-2 hidden md:table-cell">{c.alias || "-"}</td>

                  {/* CONTACTO visible solo en pantallas grandes */}
                  <td className="px-4 py-2 hidden md:table-cell">{c.contacto || "-"}</td>

                  {/* TELÉFONO + WHATSAPP */}
                  <td className="px-4 py-2">
                    <div className="flex items-center gap-2">
                      <span
                        className="truncate max-w-[50px] md:max-w-none"
                        title={c.telefono || ""}
                      >
                        {c.telefono || "-"}
                      </span>
                      {c.telefono && (
                        <button
                          onClick={() => handleWhatsApp(c.telefono)}
                          className="text-green-600 hover:text-green-700 flex-shrink-0"
                          title="Enviar mensaje por WhatsApp"
                        >
                          <MessageCircle size={18} />
                        </button>
                      )}
                    </div>
                  </td>

                  {/* EMAIL + ICONO */}
                  <td className="px-4 py-2">
                    <div className="flex items-center gap-2">
                      <span
                        className="truncate max-w-[50px] md:max-w-none"
                        title={c.email || ""}
                      >
                        {c.email || "-"}
                      </span>
                      {c.email && (
                        <button
                          onClick={() => handleEmail(c.email)}
                          className="text-blue-600 hover:text-blue-700 flex-shrink-0"
                          title="Enviar correo"
                        >
                          <Mail size={18} />
                        </button>
                      )}
                    </div>
                  </td>

                  {/* BOTONES DE ACCIÓN */}
                  <td className="px-4 py-2 text-center">
                    <div className="flex justify-center gap-3">
                      <button
                        className="bg-blue-500 hover:bg-blue-600 text-white px-3 py-1.5 rounded-md text-sm font-medium flex items-center gap-1 transition"
                        onClick={() => nav(`/clientes/editar/${c.id_cliente}`)}
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
