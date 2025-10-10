import React from "react";
import { useNavigate } from "react-router-dom";
import { Plus, FileText, Image, Users } from "lucide-react";

export default function DashboardPage() {
  const nav = useNavigate();

  const cardStyle = (bgUrl) => ({
    backgroundImage: `url(${bgUrl})`,
    backgroundSize: "cover",
    backgroundPosition: "center",
    position: "relative",
  });

  return (
    <div className="container mx-auto px-4 sm:px-6 lg:px-8 mt-6 space-y-6">
      <h2 className="text-2xl font-bold text-gray-800">Dashboard</h2>

      {/* INSPECCIONES */}
      <div className="bg-white shadow-md rounded-lg p-6 border border-gray-200 overflow-hidden" style={cardStyle("/images/inspecciones-bg.jpg")}>
        <h3 className="text-lg font-semibold text-gray-700 mb-1">Inspecciones</h3>
        <p className="text-sm text-gray-500 mb-4">Crear nuevas inspecciones o revisar las existentes.</p>
        <div className="flex flex-wrap gap-3">
          <button
            className="bg-brand hover:bg-brand-light text-white font-medium px-5 py-2 rounded-lg flex items-center gap-2 transition"
            onClick={() => nav("/inspecciones/nueva")}
          >
            <Plus size={16} /> Nueva Inspección
          </button>
          <button
            className="bg-blue-500 hover:bg-blue-600 text-white font-medium px-5 py-2 rounded-lg flex items-center gap-2 transition"
            onClick={() => nav("/inspecciones")}
          >
            <FileText size={16} /> Revisar Inspecciones
          </button>
        </div>
      </div>

      {/* REVISAR PROYECTOS */}
      <div className="bg-white shadow-md rounded-lg p-6 border border-gray-200 overflow-hidden" style={cardStyle("/images/proyectos-bg.jpg")}>
        <h3 className="text-lg font-semibold text-gray-700 mb-1">Revisar Proyectos</h3>
        <p className="text-sm text-gray-500 mb-4">Accede a todos los proyectos para revisión y seguimiento de avances.</p>
        <div className="flex flex-wrap gap-3">
          <button
            className="bg-blue-500 hover:bg-blue-600 text-white font-medium px-5 py-2 rounded-lg flex items-center gap-2 transition"
            onClick={() => nav("/proyectos")}
          >
            <FileText size={16} /> Revisar Proyectos
          </button>
        </div>
      </div>

      {/* ADMINISTRAR IMÁGENES */}
      <div className="bg-white shadow-md rounded-lg p-6 border border-gray-200 overflow-hidden" style={cardStyle("/images/imagenes-bg.jpg")}>
        <h3 className="text-lg font-semibold text-gray-700 mb-1">Administrar Imágenes</h3>
        <p className="text-sm text-gray-500 mb-4">Tomar, subir o adjuntar imágenes a proyectos e inspecciones.</p>
        <div className="flex flex-wrap gap-3">
          <button
            className="bg-gray-100 hover:bg-gray-200 text-gray-800 font-medium px-5 py-2 rounded-lg flex items-center gap-2 transition"
            onClick={() => nav("/imagenes")}
          >
            <Image size={16} /> Tomar Imágenes
          </button>
          <button
            className="bg-gray-300 hover:bg-gray-400 text-gray-800 font-medium px-5 py-2 rounded-lg flex items-center gap-2 transition"
            onClick={() => nav("/imagenes")}
          >
            <Image size={16} /> Subir Imágenes
          </button>
          <button
            className="bg-brand hover:bg-brand-light text-white font-medium px-5 py-2 rounded-lg flex items-center gap-2 transition"
            onClick={() => nav("/imagenes")}
          >
            <Image size={16} /> Adjuntar a Proyecto
          </button>
        </div>
      </div>

      {/* CLIENTES */}
      <div className="bg-white shadow-md rounded-lg p-6 border border-gray-200 overflow-hidden" style={cardStyle("/images/clientes-bg.jpg")}>
        <h3 className="text-lg font-semibold text-gray-700 mb-1">Clientes</h3>
        <p className="text-sm text-gray-500 mb-4">Ver y agregar clientes en el sistema.</p>
        <div className="flex flex-wrap gap-3">
          <button
            className="bg-blue-500 hover:bg-blue-600 text-white font-medium px-5 py-2 rounded-lg flex items-center gap-2 transition"
            onClick={() => nav("/clientes")}
          >
            <Users size={16} /> Ver Clientes
          </button>
          <button
            className="bg-brand hover:bg-brand-light text-white font-medium px-5 py-2 rounded-lg flex items-center gap-2 transition"
            onClick={() => nav("/clientes/nuevo")}
          >
            <Plus size={16} /> Nuevo Cliente
          </button>
        </div>
      </div>
    </div>
  );
}
