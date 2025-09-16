// src/pages/Clientes/ClienteFormPage.jsx
import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { ClientesAPI } from "../../services/clientes";

export default function ClienteFormPage() {
  const nav = useNavigate();
  const { id } = useParams(); // id del cliente para editar, si existe

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

  // Cargar datos si es edición
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

  if (loading) return <p>Cargando cliente...</p>;

  return (
    <div className="container mx-auto mt-6">
      <h2 className="text-2xl font-bold mb-4">
        {id ? "Editar Cliente" : "Nuevo Cliente"}
      </h2>

      {error && <p className="text-red-600 mb-4">{error}</p>}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block font-semibold">Nombre</label>
          <input
            type="text"
            name="nombre"
            value={cliente.nombre}
            onChange={handleChange}
            required
            className="input"
          />
        </div>

        <div>
          <label className="block font-semibold">Alias</label>
          <input
            type="text"
            name="alias"
            value={cliente.alias || ""}
            onChange={handleChange}
            className="input"
          />
        </div>

        <div>
          <label className="block font-semibold">Logo URL</label>
          <input
            type="text"
            name="logo_url"
            value={cliente.logo_url || ""}
            onChange={handleChange}
            className="input"
          />
        </div>

        <div>
          <label className="block font-semibold">Contacto</label>
          <input
            type="text"
            name="contacto"
            value={cliente.contacto || ""}
            onChange={handleChange}
            className="input"
          />
        </div>

        <div>
          <label className="block font-semibold">Dirección</label>
          <input
            type="text"
            name="direccion"
            value={cliente.direccion || ""}
            onChange={handleChange}
            className="input"
          />
        </div>

        <div>
          <label className="block font-semibold">Teléfono</label>
          <input
            type="text"
            name="telefono"
            value={cliente.telefono || ""}
            onChange={handleChange}
            className="input"
          />
        </div>

        <div>
          <label className="block font-semibold">Email</label>
          <input
            type="email"
            name="email"
            value={cliente.email || ""}
            onChange={handleChange}
            className="input"
          />
        </div>

        <button
          type="submit"
          className="btn"
        >
          {id ? "Actualizar Cliente" : "Crear Cliente"}
        </button>
      </form>
    </div>
  );
}
