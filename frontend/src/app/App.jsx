import React from "react";
import { BrowserRouter } from "react-router-dom";
import "../styles/global.css";
import AppRoutes from "./routes";
import Navbar from "../components/Navbar";

export default function App(){
  return (
    <BrowserRouter>
      <div className="page">
        <Navbar />
        <div className="appContent">
          <div className="container">
            <AppRoutes />
          </div>
        </div>
      </div>
    </BrowserRouter>
  );
}

