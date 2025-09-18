// Reemplaza "TU_CESIUM_TOKEN" con tu token de Cesium ION
Cesium.Ion.defaultAccessToken = "TU_CESIUM_TOKEN"; 

const viewer = new Cesium.Viewer('cesiumContainer', { terrain: Cesium.Terrain.fromWorldTerrain() });
const cotopaxi = Cesium.Cartesian3.fromDegrees(-78.436, -0.680, 5897);
viewer.camera.flyTo({ destination: Cesium.Cartesian3.fromDegrees(-78.436, -0.70, 12000) });

const pin = viewer.entities.add({
  position: cotopaxi,
  point: { pixelSize: 12 },
  label: { text: "Cotopaxi", pixelOffset: new Cesium.Cartesian2(0, -20) }
});

async function refresh() {
  const base = (window.location.origin.includes(':8080') ? window.location.origin.replace(':8080', ':8000') : window.location.origin);
  const lastTilt = await fetch(`${base.replace('http','http')}/last/tilt`).then(r=>r.json()).catch(()=>({}));
  const lastRain = await fetch(`${base}/last/rain`).then(r=>r.json()).catch(()=>({}));
  pin.label.text = `Cotopaxi\nTilt R:${lastTilt.radial_deg??'-'}° T:${lastTilt.tangential_deg??'-'}°\nRain:${lastRain.rate_mm_h??'-'} mm/h`;
  refreshEvents();
}

async function refreshEvents() {
  const base = (window.location.origin.includes(':8080') ? window.location.origin.replace(':8080', ':8000') : window.location.origin);
  const events = await fetch(`${base}/events`).then(r => r.json()).catch(() => []);
  // Limpiar eventos anteriores
  viewer.entities.values.filter(e => e.label && e.label.id && e.label.id.startsWith('event-')).forEach(e => viewer.entities.remove(e));

  events.forEach((event, i) => {
    const eventPin = viewer.entities.add({
      position: Cesium.Cartesian3.fromDegrees(-78.436, -0.680, 5897 + i * 100),
      label: {
        id: `event-${i}`,
        text: `${event.type} (${event.level})`,
        font: '12pt monospace',
        fillColor: Cesium.Color.ORANGE,
        style: Cesium.LabelStyle.FILL_AND_OUTLINE,
        outlineWidth: 2,
        verticalOrigin: Cesium.VerticalOrigin.BOTTOM,
        pixelOffset: new Cesium.Cartesian2(0, -9)
      }
    });
  });
}

setInterval(refresh, 3000);
