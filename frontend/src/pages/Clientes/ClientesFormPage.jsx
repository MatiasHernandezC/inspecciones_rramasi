import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { ClientesAPI } from "../../services/clientes";
import { ArrowLeft, Home } from "lucide-react";

export default function ClienteFormPage() {
  const nav = useNavigate();
  const { id } = useParams();

  const [cliente, setCliente] = useState({
    nombre: "",
    alias: "",
    logo_url: "",
    contacto: "",
    direccion: "",
    telefono: "",
    email: "",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (id) {
      setLoading(true);
      ClientesAPI.obtener(id)
        .then((data) => setCliente(data))
        .catch((err) => setError(err.message))
        .finally(() => setLoading(false));
    }
  }, [id]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setCliente((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      if (id) {
        await ClientesAPI.actualizar(id, cliente);
      } else {
        await ClientesAPI.crear(cliente);
      }
      nav("/clientes");
    } catch (err) {
      setError(err.message);
    }
  };

  if (loading)
    return (
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <p className="text-gray-600">Cargando cliente...</p>
      </div>
    );

  return (
    <div className="container mx-auto px-4 sm:px-6 lg:px-8">
      {/* ENCABEZADO */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-3 gap-3">
        <h2 className="text-2xl font-bold text-gray-800">
          {id ? "Editar Cliente" : "Nuevo Cliente"}
        </h2>
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
        </div>
      </div>

      {/* ERROR */}
      {error && <p className="text-red-600 mb-4">{error}</p>}

      {/* FORMULARIO */}
      <form
        onSubmit={handleSubmit}
        className="bg-white shadow-md rounded-lg p-6 border border-gray-200 grid grid-cols-1 md:grid-cols-2 gap-6"
      >
        {[
          { label: "Nombre", name: "nombre", type: "text", required: true },
          { label: "Alias", name: "alias", type: "text" },
          { label: "Logo URL", name: "logo_url", type: "text" },
          { label: "Contacto", name: "contacto", type: "text" },
          { label: "Dirección", name: "direccion", type: "text" },
          { label: "Teléfono", name: "telefono", type: "text" },
          { label: "Email", name: "email", type: "email" },
        ].map((field) => (
          <div key={field.name} className="flex flex-col">
            <label className="block font-semibold mb-1">{field.label}</label>
            <input
              type={field.type}
              name={field.name}
              value={cliente[field.name] || ""}
              onChange={handleChange}
              required={field.required}
              className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-brand focus:border-brand transition"
            />
          </div>
        ))}

        {/* Botón ocupa toda la fila */}
        <div className="md:col-span-2 flex justify-start mt-2">
          <button
            type="submit"
            className="bg-brand hover:bg-brand-light text-white font-medium px-6 py-2 rounded-lg transition"
          >
            {id ? "Actualizar Cliente" : "Crear Cliente"}
          </button>
        </div>
      </form>
    </div>
  );
}
