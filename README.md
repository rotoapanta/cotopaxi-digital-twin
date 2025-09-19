# Cotopaxi Digital Twin (Synthetic)

## Requisitos
- Docker / Docker Compose
- Token de Cesium ion (gratuito)

## Pasos
1. Copiar `.env.example` a `.env` y completar valores (incluye CESIUM_ION_TOKEN en web/app.js).
2. `docker compose up -d --build`
3. Abrir:
   - API: http://localhost:8000/docs
   - Grafana: http://localhost:3000 (admin / admin)
   - Web 3D: http://localhost:8080

## Medidas (Influx)
- tilt(radial_deg,tangential_deg), gnss(lat,lon,alt,uplift_mm),
  infrasound(pa_rms,pa_peak), rain(mm,rate_mm_h), gas(so2_ppm,co2_ppm), events(type,level,score).
