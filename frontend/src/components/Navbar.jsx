import React, { useState } from "react";
import { Link } from "react-router-dom";
import { Users, FileText, Image, Plus } from "lucide-react";

export default function Navbar() {
  const [open, setOpen] = useState(false);

  const navItems = [
    { label: "Nueva Inspección", to: "/inspecciones/nueva", icon: <Plus size={16} /> },
    { label: "Inspecciones", to: "/inspecciones", icon: <FileText size={16} /> },
    { label: "Proyectos", to: "/proyectos", icon: <FileText size={16} /> },
    { label: "Clientes", to: "/clientes", icon: <Users size={16} /> },
    { label: "Imágenes", to: "/imagenes", icon: <Image size={16} /> },
  ];

  return (
    <nav className="fixed inset-x-0 top-0 z-50 bg-blue-700 text-white shadow-md">
      <div className="mx-auto max-w-5xl px-5">
        <div className="flex h-16 items-center justify-between gap-3">
          {/* LOGO */}
          <Link
            to="/"
            className="flex items-center gap-2 text-white no-underline"
            aria-label="Inicio"
          >
            <img
              src={process.env.PUBLIC_URL + "/logo192.png"}
              alt="Logo"
              className="h-9 w-9 object-contain"
            />
            <span className="whitespace-nowrap text-lg font-extrabold tracking-tight">
              Inspecciones RRamasi
            </span>
          </Link>

          {/* MENU DESKTOP */}
          <div className="hidden sm:flex items-center gap-2">
            {navItems.map((item) => (
              <Link
                key={item.to}
                to={item.to}
                className="inline-flex items-center gap-1 rounded-lg bg-white/15 px-3 py-2 text-sm font-semibold text-white backdrop-blur hover:bg-white/25 focus:outline-none focus:ring-2 focus:ring-white/60"
              >
                {item.icon}
                {item.label}
              </Link>
            ))}
          </div>

          {/* BOTÓN MENU MÓVIL */}
          <button
            className="inline-flex h-10 w-10 items-center justify-center rounded-full bg-white/15 text-white hover:bg-white/25 focus:outline-none focus:ring-2 focus:ring-white/60 sm:hidden"
            aria-label="Abrir menú"
            onClick={() => setOpen(!open)}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="currentColor"
              className="h-6 w-6"
            >
              <path
                fillRule="evenodd"
                d="M3.75 5.25a.75.75 0 0 1 .75-.75h15a.75.75 0 0 1 0 1.5h-15a.75.75 0 0 1-.75-.75Zm0 6a.75.75 0 0 1 .75-.75h15a.75.75 0 0 1 0 1.5h-15a.75.75 0 0 1-.75-.75Zm0 6a.75.75 0 0 1 .75-.75h15a.75.75 0 0 1 0 1.5h-15a.75.75 0 0 1-.75-.75Z"
                clipRule="evenodd"
              />
            </svg>
          </button>
        </div>

        {/* MENU MÓVIL */}
        {open && (
          <div className="sm:hidden mt-2 space-y-1 bg-blue-700 rounded-lg p-2 shadow-md">
            {navItems.map((item) => (
              <Link
                key={item.to}
                to={item.to}
                className="flex items-center gap-2 px-3 py-2 rounded-md text-white font-semibold hover:bg-white/25 transition"
                onClick={() => setOpen(false)}
              >
                {item.icon}
                {item.label}
              </Link>
            ))}
          </div>
        )}
      </div>
    </nav>
  );
}
