import React from "react";
import { BrowserRouter } from "react-router-dom";
import "../styles/global.css";
import AppRoutes from "./routes";

function Header(){
  return (
    <header className="header">
      <div className="brand">
        <div className="logo">Logo</div>
        <h1 className="title">Panel de Proyectos</h1>
      </div>
      <button className="menuBtn" aria-label="Menú">⋮</button>
    </header>
  );
}

export default function App(){
  return (
    <BrowserRouter>
      <div className="page">
        <div className="container">
          <Header />
          <AppRoutes />
        </div>
      </div>
    </BrowserRouter>
  );
}
