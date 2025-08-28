import React from "react";
import { Link } from "react-router-dom";

export default function Navbar(){
  return (
    <nav className="navbar" role="navigation" aria-label="Barra principal">
      <div className="navInner">
        <div className="navRow">
          <Link to="/" className="brandLink" aria-label="Inicio">
            <img
              src={process.env.PUBLIC_URL + "/logo192.png"}
              alt="Logo"
              className="brandImg"
            />
            <span className="brandTitle">Inspecciones RRamasi</span>
          </Link>

          <div className="actions hideMobile">
            <Link to="/inspecciones/nueva" className="navBtn">Nueva Inspección</Link>
          </div>

          <button className="hamburger showMobile" aria-label="Abrir menú">☰</button>
        </div>
      </div>
    </nav>
  );
}

