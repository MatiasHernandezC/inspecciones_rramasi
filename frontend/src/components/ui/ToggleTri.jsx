import React from "react";

/** Tri-estado: PASA / FALLA / N/A  */
export default function ToggleTri({ value, onChange, name }){
  const opts = [
    { k: "PASA", v: "P" },
    { k: "FALLA", v: "F" },
    { k: "N/A", v: "N" },
  ];
  return (
    <div className="radioRow" role="radiogroup" aria-label={name}>
      {opts.map(o => (
        <label key={o.v}>
          <input
            type="radio"
            name={name}
            checked={value === o.v}
            onChange={() => onChange(o.v)}
          />
          <span>{o.k}</span>
        </label>
      ))}
    </div>
  );
}
