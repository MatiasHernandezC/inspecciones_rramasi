import React from "react";
import { BrowserRouter } from "react-router-dom";
import "../styles/global.css";
import AppRoutes from "./routes";
import Navbar from "../components/Navbar";

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-slate-50 text-slate-900">
        <Navbar />
        <div className="pt-20">
          <div className="mx-auto max-w-5xl px-5 pb-20">
            <AppRoutes />
          </div>
        </div>
      </div>
    </BrowserRouter>
  );
}
