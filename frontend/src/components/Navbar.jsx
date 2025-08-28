import React from "react";
import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav
      className="fixed inset-x-0 top-0 z-50 bg-blue-700 text-white shadow-md"
      role="navigation"
      aria-label="Barra principal"
    >
      <div className="mx-auto max-w-5xl px-5">
        <div className="flex h-16 items-center justify-between gap-3">
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

          <div className="hidden items-center gap-2 sm:flex">
            <Link
              to="/inspecciones/nueva"
              className="inline-flex items-center rounded-lg bg-white/15 px-3 py-2 text-sm font-semibold text-white backdrop-blur hover:bg-white/25 focus:outline-none focus:ring-2 focus:ring-white/60"
            >
              Nueva Inspección
            </Link>
          </div>

          <button
            className="inline-flex h-10 w-10 items-center justify-center rounded-full bg-white/15 text-white hover:bg-white/25 focus:outline-none focus:ring-2 focus:ring-white/60 sm:hidden"
            aria-label="Abrir menú"
            type="button"
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
      </div>
    </nav>
  );
}

