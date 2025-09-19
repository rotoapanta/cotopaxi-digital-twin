(async function () {
  const apiBase = location.origin.includes(':8080')
    ? location.origin.replace(':8080', ':8000')
    : location.origin;

  // 1) Token desde backend
  const r = await fetch(`${apiBase}/config/cesium-token`);
  const { token } = await r.json();
  Cesium.Ion.defaultAccessToken = token;
  const showErr = (msg) => {
    try {
      const el = document.getElementById('err');
      el.textContent = msg;
      el.style.display = 'block';
    } catch(_) {}
  };
  if (!token) {
    showErr('Cesium Ion token vacío: no se podrá cargar el terreno. Verifica CESIUM_ION_TOKEN y restricciones de dominio.');
  }

  // 2) Providers (Ion)
  // Terreno real 3D: Cesium World Terrain (requiere token). Fallback a elipsoide si falla.
  const terrainProvider = await (async () => {
    try {
      return await Cesium.createWorldTerrainAsync();
    } catch (e) {
      showErr('No se pudo cargar Cesium World Terrain. Usando elipsoidal.');
      return new Cesium.EllipsoidTerrainProvider();
    }
  })();

  // Capa base: usar el mismo provider estable que en test (OpenStreetMapImageryProvider)
  let baseImagery = null;
  try {
    baseImagery = new Cesium.OpenStreetMapImageryProvider({
      url: 'https://a.tile.openstreetmap.org/' // Cesium maneja subdominios
    });
  } catch (e) {
    showErr('No se pudo crear OSM como base. Probando Esri World Imagery (tiles).');
  }
  if (!baseImagery) {
    try {
      baseImagery = new Cesium.UrlTemplateImageryProvider({
        url: 'https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
      });
    } catch (e) {
      showErr('Falló también Esri World Imagery como base.');
    }
  }

  // 3) Viewer
  const viewer = new Cesium.Viewer("cesiumContainer", {
    terrainProvider,
    imageryProvider: false,
    baseLayerPicker: false,
    geocoder: false,
    animation: false,
    timeline: false
  });

  // Ajustes para resaltar el relieve del Cotopaxi
  try { viewer.scene.globe.terrainExaggeration = 1.35; } catch(_) {}
  viewer.scene.globe.depthTestAgainstTerrain = true;
  viewer.scene.globe.enableLighting = true;
  viewer.scene.msaaSamples = 4;

  // Añadir capa base ahora, igual que en test.html
  if (baseImagery) {
    viewer.imageryLayers.addImageryProvider(baseImagery);
  } else {
    try {
      const osmInit = new Cesium.OpenStreetMapImageryProvider({
        url: 'https://a.tile.openstreetmap.org/'
      });
      viewer.imageryLayers.addImageryProvider(osmInit);
    } catch (e) {
      showErr('No se pudo crear OSM tras iniciar el visor. Probando Esri tiles.');
      try {
        const esriInit = new Cesium.UrlTemplateImageryProvider({
          url: 'https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
        });
        viewer.imageryLayers.addImageryProvider(esriInit);
      } catch (e2) {
        showErr('Falló también Esri tras iniciar el visor.');
      }
    }
  }

  if (terrainProvider && terrainProvider.errorEvent) {
    terrainProvider.errorEvent.addEventListener(function() {
      showErr("Error cargando terreno Ion. Cambiando a elipsoidal.");
      viewer.terrainProvider = new Cesium.EllipsoidTerrainProvider();
    });
  }

  // Evitar overlay de Cesium y recuperar ante errores de render (e.g., provider roto)
  viewer.cesiumWidget.showRenderLoopErrors = false;
  viewer.scene.renderError.addEventListener(function(err){
    showErr('Render error: ' + (err && err.message ? err.message : err));
    try {
      // Quitar capas problemáticas y usar OSM (mismo provider que en test)
      viewer.imageryLayers.removeAll(false);
      viewer.terrainProvider = new Cesium.EllipsoidTerrainProvider();
      const osmSafe = new Cesium.OpenStreetMapImageryProvider({
        url: 'https://a.tile.openstreetmap.org/'
      });
      viewer.imageryLayers.addImageryProvider(osmSafe);
    } catch(_) {}
  });

  
  // 4) Cámara y entidad
  viewer.camera.flyTo({
    destination: Cesium.Cartesian3.fromDegrees(-78.436, -0.680, 12000),
    orientation: {
      heading: Cesium.Math.toRadians(0),
      pitch: Cesium.Math.toRadians(-60),
      roll: 0
    }
  });

  const pin = viewer.entities.add({
    position: Cesium.Cartesian3.fromDegrees(-78.436, -0.680, 5897),
    point: { pixelSize: 12 },
    label: { text: "Cotopaxi\nCargando…", showBackground: true }
  });

  // 5) Refresco de datos
  const get = async (u)=>{ try{ const x=await fetch(u); return await x.json(); }catch{ return {}; } };
  async function refresh(){
    const tilt = await get(`${apiBase}/last/tilt`);
    const rain = await get(`${apiBase}/last/rain`);
    const r = tilt.values?.radial_deg ?? "-";
    const t = tilt.values?.tangential_deg ?? "-";
    const rr = rain.values?.rate_mm_h ?? "-";
    pin.label.text = `Cotopaxi\nTilt R:${r}°  T:${t}°\nRain: ${rr} mm/h`;
  }
  refresh();
  setInterval(refresh, 3000);
})();
