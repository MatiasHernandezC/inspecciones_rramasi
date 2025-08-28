import React, { useRef } from "react";

export default function GestorImagenesPage(){
  const fileRef = useRef(null);
  return (
    <div>
      <h2 className="title" style={{fontSize:32}}>Gestor de Imágenes</h2>
      <div className="section">
        <div className="row">
          <button className="btn" onClick={()=>fileRef.current?.click()}>Subir imágenes</button>
          <input ref={fileRef} type="file" accept="image/*" multiple style={{display:'none'}} onChange={(e)=>{
            const files = Array.from(e.target.files || []);
            if(!files.length) return; alert(`Subidas ${files.length} imágenes (simulado)`);
          }} />
        </div>
      </div>
    </div>
  );
}
