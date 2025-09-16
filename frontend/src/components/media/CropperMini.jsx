import React, { useEffect, useRef, useState } from "react";

export default function CropperMini({ onCropped, size = 512 }) {
  const [src, setSrc] = useState(null);
  const [preview, setPreview] = useState(null);
  const canvasRef = useRef(null);

  useEffect(() => {
    if (!src) return;
    const img = new Image();
    img.onload = () => {
      const s = Math.min(img.width, img.height);
      const sx = (img.width - s) / 2;
      const sy = (img.height - s) / 2;
      const canvas = canvasRef.current;
      canvas.width = size;
      canvas.height = size;
      const ctx = canvas.getContext("2d");
      ctx.clearRect(0, 0, size, size);
      ctx.drawImage(img, sx, sy, s, s, 0, 0, size, size);
      setPreview(canvas.toDataURL("image/jpeg", 0.9));
    };
    img.src = src;
  }, [src, size]);

  const onFile = (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => setSrc(reader.result);
    reader.readAsDataURL(file);
  };

  const doCrop = () => {
    if (!canvasRef.current) return;
    const dataUrl = canvasRef.current.toDataURL("image/jpeg", 0.9);
    onCropped?.(dataUrl);
    setPreview(dataUrl);
  };

  const reset = () => {
    setSrc(null);
    setPreview(null);
  };

  return (
    <div className="cropper-mini" style={{ maxWidth: 360 }}>
      <input type="file" accept="image/*" onChange={onFile} />
      {src && (
        <div style={{ marginTop: 8, textAlign: "center" }}>
          <canvas
            ref={canvasRef}
            style={{
              maxWidth: "100%",
              border: "1px solid #ccc",
              borderRadius: 8,
              background: "#f5f5f5",
            }}
          />
        </div>
      )}

      <div className="row" style={{ marginTop: 8, gap: 8 }}>
        <button className="btn" disabled={!src} onClick={doCrop}>
          Recortar
        </button>
        <button className="btn secondary" disabled={!src} onClick={reset}>
          Reset
        </button>
      </div>

      {preview && (
        <div style={{ marginTop: 8, textAlign: "center" }}>
          <h4 style={{ fontSize: 14, color: "#555" }}>Vista previa</h4>
          <img
            src={preview}
            alt="Preview"
            style={{ maxWidth: "100%", borderRadius: 6, border: "1px solid #ccc" }}
          />
        </div>
      )}
    </div>
  );
}
