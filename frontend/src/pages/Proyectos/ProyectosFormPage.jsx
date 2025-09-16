import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { ProyectosAPI } from "../../services/proyectos";
import { ClientesAPI } from "../../services/clientes";

export default function ProyectoFormPage() {
  const { id } = useParams();
  const nav = useNavigate();
  const [clientes, setClientes] = useState([]);
  const [form, setForm] = useState({
    id_cliente: "",
    nombre: "",
    numero: "",
    descripcion: "",
    estado: "",
  });

  useEffect(() => {
    ClientesAPI.listar({}).then(setClientes);

    if (id) {
      ProyectosAPI.obtener(id).then(p => setForm({
        id_cliente: p.id_cliente,
        nombre: p.nombre,
        numero: p.numero || "",
        descripcion: p.descripcion || "",
        estado: p.estado || "",
      }));
    }
  }, [id]);

  const handleChange = e => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async e => {
    e.preventDefault();
    if (id) await ProyectosAPI.actualizar(id, form);
    else await ProyectosAPI.crear(form);
    nav("/proyectos");
  };

  return (
    <div className="p-6 max-w-3xl mx-auto bg-white shadow rounded-lg">
      <h2 className="text-2xl font-bold mb-6">{id ? "Editar Proyecto" : "Nuevo Proyecto"}</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Cliente</label>
          <select name="id_cliente" value={form.id_cliente} onChange={handleChange} className="input w-full">
            <option value="">Selecciona un cliente</option>
            {clientes.map(c => (
              <option key={c.id_cliente} value={c.id_cliente}>{c.nombre}</option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Nombre</label>
          <input type="text" name="nombre" value={form.nombre} onChange={handleChange} className="input w-full" />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Número</label>
          <input type="text" name="numero" value={form.numero} onChange={handleChange} className="input w-full" />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Estado</label>
          <input type="text" name="estado" value={form.estado} onChange={handleChange} className="input w-full" />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Descripción</label>
          <textarea name="descripcion" value={form.descripcion} onChange={handleChange} className="input w-full" rows={3}></textarea>
        </div>

        <div className="flex justify-end gap-2 mt-4">
          <button type="button" className="btn btn-secondary" onClick={() => nav("/proyectos")}>Cancelar</button>
          <button type="submit" className="btn btn-primary">Guardar</button>
        </div>
      </form>
    </div>
  );
}
