import React, { useEffect, useMemo, useRef, useState } from "react";

export default function CellSelect({
  value,
  onChange,
  options = [],
  placeholder = "—",
  className = "",
}) {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [highlight, setHighlight] = useState(0);
  const rootRef = useRef(null);
  const inputRef = useRef(null);

  const optList = useMemo(() => {
    // normaliza opciones a strings
    return (options || []).map((o) => (typeof o === "string" ? o : String(o)));
  }, [options]);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return optList;
    return optList.filter((o) => String(o).toLowerCase().includes(q));
  }, [optList, query]);

  useEffect(() => {
    function onDoc(e) {
      if (!rootRef.current?.contains(e.target)) setOpen(false);
    }
    document.addEventListener("mousedown", onDoc);
    return () => document.removeEventListener("mousedown", onDoc);
  }, []);

  function onKeyDown(e) {
    if (e.key === "F2" || (e.altKey && e.key === "ArrowDown")) {
      e.preventDefault();
      setOpen(true);
      setTimeout(() => inputRef.current?.focus(), 0);
      return;
    }
    if (!open) return;
    if (e.key === "ArrowDown") {
      e.preventDefault();
      setHighlight((i) => Math.min(i + 1, Math.max(filtered.length - 1, 0)));
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setHighlight((i) => Math.max(i - 1, 0));
    } else if (e.key === "Enter") {
      e.preventDefault();
      const pick = filtered[highlight];
      if (pick != null) {
        onChange(pick);
        setOpen(false);
        setQuery("");
      }
    } else if (e.key === "Escape") {
      e.preventDefault();
      setOpen(false);
      setQuery("");
    } else if (e.key === "Delete") {
      e.preventDefault();
      onChange("");
      setQuery("");
      setOpen(false);
    }
  }

  function pickOption(opt) {
    onChange(opt);
    setOpen(false);
    setQuery("");
  }

  return (
    <div
      ref={rootRef}
      className={`excel-cell-select relative ${className}`}
      tabIndex={0}
      onKeyDown={onKeyDown}
    >
      <div
        className="excel-cell input flex items-center justify-between cursor-default"
        onClick={() => {
          setOpen((o) => !o);
          setTimeout(() => inputRef.current?.focus(), 0);
        }}
        title={String(value || "")}
      >
        <span className="truncate">{value || placeholder}</span>
        <span className="ml-2 opacity-60">▾</span>
      </div>

      {open && (
        <div
          className="excel-dropdown absolute z-50 mt-1 w-full rounded-md border bg-white shadow-lg"
          style={{ minWidth: "100%", maxHeight: 220, overflow: "auto" }}
        >
          <div className="px-2 py-2 border-b">
            <input
              ref={inputRef}
              className="w-full outline-none text-sm"
              placeholder="Filtrar…"
              value={query}
              onChange={(e) => {
                setQuery(e.target.value);
                setHighlight(0);
              }}
              onKeyDown={onKeyDown}
            />
          </div>
          <ul className="py-1 text-sm">
            {filtered.length === 0 ? (
              <li className="px-3 py-2 text-slate-500 select-none">Sin resultados</li>
            ) : (
              filtered.map((opt, idx) => (
                <li
                  key={String(opt)}
                  className={`px-3 py-2 cursor-pointer ${
                    idx === highlight ? "bg-blue-600 text-white" : "hover:bg-slate-100"
                  }`}
                  onMouseEnter={() => setHighlight(idx)}
                  onMouseDown={(e) => {
                    e.preventDefault();
                    pickOption(opt);
                  }}
                >
                  {String(opt)}
                </li>
              ))
            )}
          </ul>
        </div>
      )}
    </div>
  );
}

