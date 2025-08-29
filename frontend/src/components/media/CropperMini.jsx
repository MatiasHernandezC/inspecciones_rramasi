import React, { useEffect, useRef, useState } from "react";

// Mínimo viable: recorta al centro en formato 1:1, con tamaño configurable
export default function CropperMini({ onCropped, size = 512 }){
  const [src, setSrc] = useState(null);
  const imgRef = useRef(null);
  const canvasRef = useRef(null);

  useEffect(()=>{
    if(!src) return;
    const img = new Image();
    img.onload = () => {
      // calcular rectángulo centrado 1:1
      const s = Math.min(img.width, img.height);
      const sx = (img.width - s) / 2;
      const sy = (img.height - s) / 2;
      const canvas = canvasRef.current;
      canvas.width = size;
      canvas.height = size;
      const ctx = canvas.getContext("2d");
      ctx.clearRect(0,0,size,size);
      ctx.drawImage(img, sx, sy, s, s, 0, 0, size, size);
    };
    img.src = src;
  }, [src, size]);

  const onFile = (e) => {
    const f = e.target.files?.[0];
    if(!f) return;
    const reader = new FileReader();
    reader.onload = () => setSrc(reader.result);
    reader.readAsDataURL(f);
  };

  const doCrop = () => {
    if(!canvasRef.current) return;
    const dataUrl = canvasRef.current.toDataURL("image/jpeg", 0.9);
    onCropped?.(dataUrl);
  };

  return (
    <div>
      <input type="file" accept="image/*" onChange={onFile} />
      <div style={{marginTop:8}}>
        <canvas ref={canvasRef} style={{maxWidth:"100%", border:"1px solid #ccc"}} />
      </div>
      <div className="row" style={{marginTop:8}}>
        <button className="btn" disabled={!src} onClick={doCrop}>Recortar (centro 1:1)</button>
      </div>
    </div>
  );
}

